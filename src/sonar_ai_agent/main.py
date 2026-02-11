"""
Main entry point for Sonar AI Agent
"""

import argparse
import json
import os
import sys
import subprocess
from typing import Dict, Optional

from .config import Config
from .sonar.client import SonarQubeClient
from .analyzer.triage import IssueTriage
from .analyzer.context_extractor import ContextExtractor
from .analyzer.gemini_client import GeminiClient
from .patcher.patch_validator import PatchValidator
from .patcher.patch_applier import PatchApplier
from .report.generator import ReportGenerator
from .utils.logger import setup_root_logger, get_logger

logger = get_logger(__name__)


class SonarAIAgent:
    """Main Sonar AI Agent orchestrator"""
    
    def __init__(self, config: Config):
        """
        Initialize agent with configuration
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.sonar_client = SonarQubeClient(
            host_url=config.sonar_host_url,
            token=config.sonar_token,
            project_key=config.sonar_project_key,
        )
        self.gemini_client = GeminiClient(
            api_key=config.gemini_api_key, 
            model=config.gemini_model
        )
        self.context_extractor = ContextExtractor(repo_path=config.repo_path)
        self.patch_validator = PatchValidator(max_changed_lines=config.max_changed_lines)
        self.patch_applier = PatchApplier(repo_path=config.repo_path, dry_run=config.dry_run)
        self.report_generator = ReportGenerator()
    
    def run(self) -> bool:
        """
        Run the complete analysis workflow
        
        Returns:
            True if successful
        """
        try:
            logger.info("=" * 60)
            logger.info("🤖 Sonar AI Agent - Starting Analysis")
            logger.info("=" * 60)
            
            # Step 1: Fetch SonarQube data
            logger.info("\n📥 Step 1: Fetching SonarQube data...")
            sonar_data = self.sonar_client.fetch_all_data(max_issues=self.config.max_issues)
            
            # Save raw data
            self._save_json("sonar_bundle.json", {
                "quality_gate": {
                    "status": sonar_data.quality_gate.status,
                    "conditions": sonar_data.quality_gate.conditions,
                },
                "metrics": {
                    "bugs": sonar_data.metrics.bugs,
                    "vulnerabilities": sonar_data.metrics.vulnerabilities,
                    "code_smells": sonar_data.metrics.code_smells,
                    "security_hotspots": sonar_data.metrics.security_hotspots,
                    "coverage": sonar_data.metrics.coverage,
                    "duplicated_lines_density": sonar_data.metrics.duplicated_lines_density,
                    "ncloc": sonar_data.metrics.ncloc,
                },
                "total_issues": len(sonar_data.issues),
            })
            
            if not sonar_data.issues:
                logger.info("✅ No issues found! Project is clean.")
                return True
            
            # Step 2: Triage issues
            logger.info("\n🎯 Step 2: Triaging issues...")
            triaged_issues = IssueTriage.triage_issues(sonar_data.issues)
            top_issues = IssueTriage.select_top_issues(triaged_issues, self.config.max_issues)
            
            # Step 3: Extract code context (optional - skip if files not available)
            logger.info("\n📝 Step 3: Extracting code context...")
            contexts = {}
            try:
                contexts = self.context_extractor.extract_batch(
                    top_issues,
                    sonar_data.project_key,
                    max_files=self.config.max_files,
                )
            except Exception as e:
                logger.warning(f"Could not extract code context (files not available): {e}")
                logger.info("Continuing with SonarQube data only...")
            
            # Save contexts (even if empty)
            self._save_json("code_context.json", {
                key: context.to_dict()
                for key, context in contexts.items()
            })
            
            # Step 4: AI Analysis with Gemini
            logger.info("\n🧠 Step 4: Running AI analysis with Gemini...")
            analysis = self.gemini_client.analyze(sonar_data, triaged_issues, contexts)
            
            # Step 5: Validate and apply patches
            logger.info("\n🔧 Step 5: Processing patches...")
            raw_patches = analysis.get_patches()
            
            if raw_patches:
                valid_patches = self.patch_validator.validate_batch(raw_patches)
                patch_results = self.patch_applier.apply_batch(valid_patches)
            else:
                logger.info("No patches generated (normal when code context is unavailable)")
                patch_results = []
            
            # Step 6: Run Maven tests (if applicable)
            test_results = None
            if patch_results and not self.config.dry_run:
                logger.info("\n🧪 Step 6: Running Maven tests...")
                test_results = self._run_maven_tests()
            
            # Step 7: Generate report
            logger.info("\n📄 Step 7: Generating report...")
            report_path = self.report_generator.generate(
                sonar_data=sonar_data,
                triaged_issues=triaged_issues,
                analysis=analysis,
                patch_results=patch_results,
                test_results=test_results,
                dry_run=self.config.dry_run,
            )
            
            # Summary
            logger.info("\n" + "=" * 60)
            logger.info("✅ Analysis Complete!")
            logger.info("=" * 60)
            logger.info(f"📊 Report: {report_path}")
            logger.info(f"📦 SonarQube Data: sonar_bundle.json")
            logger.info(f"📝 Code Context: code_context.json")
            
            if self.config.dry_run:
                logger.info("\n⚠️  DRY RUN MODE - No changes were applied")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error during execution: {e}", exc_info=True)
            return False
    
    def _save_json(self, filename: str, data: Dict):
        """Save data to JSON file"""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"💾 Saved: {filename}")
        except Exception as e:
            logger.warning(f"Failed to save {filename}: {e}")
    
    def _run_maven_tests(self) -> Optional[Dict]:
        """
        Run Maven tests
        
        Returns:
            Dictionary with test results or None if not applicable
        """
        # Check if Maven project
        pom_path = os.path.join(self.config.repo_path, "pom.xml")
        if not os.path.exists(pom_path):
            logger.info("No pom.xml found, skipping Maven tests")
            return None
        
        try:
            result = subprocess.run(
                ["mvn", "test"],
                cwd=self.config.repo_path,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes
            )
            
            success = result.returncode == 0
            
            return {
                "success": success,
                "output": result.stdout[-500:] if result.stdout else "",
                "error": result.stderr[-500:] if result.stderr else "",
            }
            
        except subprocess.TimeoutExpired:
            logger.warning("Maven tests timed out")
            return {"success": False, "output": "", "error": "Timeout"}
        except FileNotFoundError:
            logger.warning("Maven not found")
            return None
        except Exception as e:
            logger.error(f"Error running Maven tests: {e}")
            return {"success": False, "output": "", "error": str(e)}


def main():
    """Main entry point"""
    setup_root_logger()
    
    parser = argparse.ArgumentParser(
        description="Sonar AI Agent - Automated Code Quality Review"
    )
    parser.add_argument(
        "command",
        choices=["run"],
        help="Command to execute"
    )
    parser.add_argument(
        "--repo-path",
        default=".",
        help="Path to repository (default: current directory)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run in dry-run mode (no patches applied)"
    )
    
    args = parser.parse_args()
    
    # Load configuration
    try:
        config = Config.from_env(
            dry_run=args.dry_run,
            repo_path=args.repo_path,
        )
        config.validate()
    except Exception as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    
    # Run agent
    agent = SonarAIAgent(config)
    success = agent.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
