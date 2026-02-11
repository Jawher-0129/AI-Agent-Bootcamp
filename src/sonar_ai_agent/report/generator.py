"""
Markdown report generator
"""

from datetime import datetime
from typing import List, Dict
from ..sonar.models import SonarData, Priority
from ..analyzer.gemini_client import GeminiAnalysis
from ..patcher.patch_applier import PatchResult
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ReportGenerator:
    """Generates professional Markdown reports"""
    
    def __init__(self, output_path: str = "sonar_ai_report.md"):
        """
        Initialize report generator
        
        Args:
            output_path: Path to output report file
        """
        self.output_path = output_path
    
    def generate(
        self,
        sonar_data: SonarData,
        triaged_issues: Dict[Priority, List],
        analysis: GeminiAnalysis,
        patch_results: List[PatchResult],
        test_results: Dict = None,
        dry_run: bool = False,
    ) -> str:
        """
        Generate comprehensive Markdown report
        
        Args:
            sonar_data: SonarQube data
            triaged_issues: Triaged issues
            analysis: Gemini analysis
            patch_results: Patch application results
            test_results: Test execution results
            dry_run: Whether this was a dry run
        
        Returns:
            Path to generated report
        """
        logger.info(f"Generating report: {self.output_path}")
        
        report = []
        
        # Header
        report.append(self._generate_header(sonar_data, dry_run))
        
        # Executive Summary
        report.append(self._generate_executive_summary(analysis, sonar_data))
        
        # Health Snapshot
        report.append(self._generate_health_snapshot(sonar_data))
        
        # Triage
        report.append(self._generate_triage(triaged_issues, analysis))
        
        # Root Cause Analysis
        report.append(self._generate_root_causes(analysis))
        
        # Architectural Issues
        report.append(self._generate_architectural_issues(analysis))
        
        # System Inconsistencies
        report.append(self._generate_system_inconsistencies(analysis))
        
        # Security Deep Dive
        report.append(self._generate_security_deep_dive(analysis))
        
        # Performance Optimizations
        report.append(self._generate_performance_optimizations(analysis))
        
        # Code Improvements
        report.append(self._generate_code_improvements(analysis))
        
        # Best Practices Violations
        report.append(self._generate_best_practices_violations(analysis))
        
        # SonarQube Gaps
        report.append(self._generate_sonarqube_gaps(analysis))
        
        # Recommendations
        report.append(self._generate_recommendations(analysis))
        
        # Optimizations
        report.append(self._generate_optimizations(analysis))
        
        # Patch Summary
        report.append(self._generate_patch_summary(patch_results, dry_run))
        
        # Test Verification
        if test_results:
            report.append(self._generate_test_verification(test_results))
        
        # Footer
        report.append(self._generate_footer())
        
        # Write report
        content = "\n\n".join(report)
        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        logger.info(f"✓ Report generated: {self.output_path}")
        return self.output_path
    
    def _generate_header(self, sonar_data: SonarData, dry_run: bool) -> str:
        """Generate report header"""
        mode = "🔍 DRY RUN MODE" if dry_run else "🚀 PRODUCTION MODE"
        
        return f"""# 🤖 Sonar AI Agent - Code Quality Report

**Project:** `{sonar_data.project_key}`  
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Mode:** {mode}  
**Quality Gate:** {"✅ PASSED" if sonar_data.quality_gate.is_passing() else "❌ FAILED"}

---"""
    
    def _generate_executive_summary(self, analysis: GeminiAnalysis, sonar_data: SonarData) -> str:
        """Generate executive summary"""
        summary = "Executive summary not available."
        
        if analysis.parsed_data:
            summary = analysis.parsed_data.get("executive_summary", summary)
        
        total_issues = len(sonar_data.issues)
        critical = len(sonar_data.get_critical_issues())
        
        return f"""## 📊 Executive Summary

{summary}

**Key Findings:**
- Total Issues: **{total_issues}**
- Critical Issues: **{critical}** (P0/P1)
- Code Coverage: **{sonar_data.metrics.coverage:.1f}%**
- Technical Debt: **{sonar_data.metrics.code_smells}** code smells"""
    
    def _generate_health_snapshot(self, sonar_data: SonarData) -> str:
        """Generate health snapshot"""
        metrics = sonar_data.metrics
        
        # Calculate health score (simplified)
        coverage_score = min(100, metrics.coverage)
        bug_score = max(0, 100 - metrics.bugs * 2)
        vuln_score = max(0, 100 - metrics.vulnerabilities * 5)
        duplication_score = max(0, 100 - metrics.duplicated_lines_density * 2)
        
        health_score = (coverage_score + bug_score + vuln_score + duplication_score) / 4
        
        health_emoji = "🟢" if health_score >= 80 else "🟡" if health_score >= 60 else "🔴"
        
        return f"""## {health_emoji} Health Snapshot

| Metric | Value | Status |
|--------|-------|--------|
| **Bugs** | {metrics.bugs} | {"✅" if metrics.bugs < 5 else "⚠️" if metrics.bugs < 20 else "❌"} |
| **Vulnerabilities** | {metrics.vulnerabilities} | {"✅" if metrics.vulnerabilities == 0 else "❌"} |
| **Code Smells** | {metrics.code_smells} | {"✅" if metrics.code_smells < 50 else "⚠️" if metrics.code_smells < 200 else "❌"} |
| **Security Hotspots** | {metrics.security_hotspots} | {"✅" if metrics.security_hotspots == 0 else "⚠️"} |
| **Code Coverage** | {metrics.coverage:.1f}% | {"✅" if metrics.coverage >= 80 else "⚠️" if metrics.coverage >= 60 else "❌"} |
| **Code Duplication** | {metrics.duplicated_lines_density:.1f}% | {"✅" if metrics.duplicated_lines_density < 3 else "⚠️" if metrics.duplicated_lines_density < 5 else "❌"} |
| **Lines of Code** | {metrics.ncloc:,} | ℹ️ |

**Overall Health Score:** {health_emoji} **{health_score:.1f}/100**"""
    
    def _generate_triage(self, triaged_issues: Dict[Priority, List], analysis: GeminiAnalysis) -> str:
        """Generate triage section"""
        sections = []
        
        sections.append("## 🎯 Issue Triage")
        
        priority_info = {
            Priority.P0: ("🔴", "Critical - Immediate Action Required"),
            Priority.P1: ("🟡", "High - Critical Technical Debt"),
            Priority.P2: ("🟢", "Medium - Optimizations"),
        }
        
        for priority in [Priority.P0, Priority.P1, Priority.P2]:
            emoji, description = priority_info[priority]
            issues = triaged_issues.get(priority, [])
            
            sections.append(f"\n### {emoji} {priority.value}: {description}")
            sections.append(f"\n**Count:** {len(issues)} issues\n")
            
            if issues[:5]:  # Show top 5
                sections.append("**Top Issues:**")
                for i, issue in enumerate(issues[:5], 1):
                    sections.append(
                        f"{i}. [{issue.type.value}] {issue.message[:80]}... "
                        f"(`{issue.rule}`)"
                    )
        
        return "\n".join(sections)
    
    def _generate_root_causes(self, analysis: GeminiAnalysis) -> str:
        """Generate root cause analysis"""
        sections = ["## 🔍 Root Cause Analysis"]
        
        root_causes = analysis.get_root_causes()
        
        if not root_causes:
            sections.append("\n*No root cause analysis available.*")
            return "\n".join(sections)
        
        for i, cause in enumerate(root_causes, 1):
            category = cause.get("category", "Unknown")
            description = cause.get("description", "")
            affected = cause.get("affected_issues", [])
            impact = cause.get("impact", "")
            
            sections.append(f"\n### {i}. {category}")
            sections.append(f"\n**Description:** {description}")
            sections.append(f"\n**Affected Issues:** {len(affected)}")
            sections.append(f"\n**Impact:** {impact}")
        
        return "\n".join(sections)
    
    def _generate_recommendations(self, analysis: GeminiAnalysis) -> str:
        """Generate recommendations"""
        sections = ["## 💡 Recommendations"]
        
        recommendations = analysis.get_recommendations()
        
        if not recommendations:
            sections.append("\n*No recommendations available.*")
            return "\n".join(sections)
        
        for i, rec in enumerate(recommendations[:10], 1):  # Top 10
            title = rec.get("title", "Recommendation")
            priority = rec.get("priority", "P2")
            category = rec.get("category", "GENERAL")
            benefit = rec.get("benefit", "")
            effort = rec.get("effort", "Unknown")
            action = rec.get("action", "")
            implementation_code = rec.get("implementation_code", "")
            
            priority_emoji = {"P0": "🔴", "P1": "🟡", "P2": "🟢"}.get(priority, "⚪")
            
            sections.append(f"\n### {priority_emoji} {i}. {title}")
            sections.append(f"\n**Priority:** {priority} | **Category:** {category} | **Effort:** {effort}")
            sections.append(f"\n**Benefit:** {benefit}")
            sections.append(f"\n**Action:** {action}")
            
            if implementation_code:
                sections.append("\n**Implementation:**\n```java\n" + implementation_code + "\n```")
        
        return "\n".join(sections)
    
    def _generate_optimizations(self, analysis: GeminiAnalysis) -> str:
        """Generate optimizations"""
        sections = ["## ⚡ Optimizations"]
        
        optimizations = analysis.get_optimizations()
        
        # Quick Wins
        quick_wins = optimizations.get("quick_wins", [])
        if quick_wins:
            sections.append("\n### 🚀 Quick Wins (≤ 30 min)")
            for i, opt in enumerate(quick_wins[:5], 1):
                title = opt.get("title", "")
                minutes = opt.get("effort_minutes", "?")
                benefit = opt.get("benefit", "")
                code = opt.get("code", "")
                sections.append(f"\n{i}. **{title}** ({minutes} min) - {benefit}")
                if code:
                    sections.append("```java\n" + code + "\n```")
        
        # Safe Refactors
        safe_refactors = optimizations.get("safe_refactors", [])
        if safe_refactors:
            sections.append("\n### 🛠️ Safe Refactors")
            for i, opt in enumerate(safe_refactors[:5], 1):
                title = opt.get("title", "")
                description = opt.get("description", "")
                code = opt.get("code", "")
                sections.append(f"\n{i}. **{title}** - {description}")
                if code:
                    sections.append("```java\n" + code + "\n```")
        
        # Strategic
        strategic = optimizations.get("strategic", [])
        if strategic:
            sections.append("\n### 📈 Strategic Improvements")
            for i, opt in enumerate(strategic[:3], 1):
                title = opt.get("title", "")
                description = opt.get("description", "")
                long_term = opt.get("long_term_value", "")
                plan = opt.get("implementation_plan", [])
                sections.append(f"\n{i}. **{title}** - {description}")
                if long_term:
                    sections.append(f"\n   *Long-term value:* {long_term}")
                if plan:
                    sections.append("\n   **Implementation Plan:**")
                    for step in plan:
                        sections.append(f"   - {step}")
        
        if not quick_wins and not safe_refactors and not strategic:
            sections.append("\n*No optimization suggestions available.*")
        
        return "\n".join(sections)
    
    def _generate_patch_summary(self, patch_results: List[PatchResult], dry_run: bool) -> str:
        """Generate patch summary"""
        sections = ["## 🔧 Patch Summary"]
        
        if not patch_results:
            sections.append("\n*No patches generated.*")
            return "\n".join(sections)
        
        successful = [r for r in patch_results if r.success]
        failed = [r for r in patch_results if not r.success]
        
        sections.append(f"\n**Total Patches:** {len(patch_results)}")
        sections.append(f"**Successful:** ✅ {len(successful)}")
        sections.append(f"**Failed:** ❌ {len(failed)}")
        
        if dry_run:
            sections.append("\n> **Note:** This was a DRY RUN. No changes were applied.")
        
        if successful:
            sections.append("\n### ✅ Applied Patches")
            for result in successful[:10]:
                sections.append(f"- `{result.file_path}` - {result.message}")
        
        if failed:
            sections.append("\n### ❌ Failed Patches")
            for result in failed:
                error = result.error or "Unknown error"
                sections.append(f"- `{result.file_path}` - {error}")
        
        return "\n".join(sections)
    
    def _generate_test_verification(self, test_results: Dict) -> str:
        """Generate test verification"""
        sections = ["## 🧪 Test Verification"]
        
        success = test_results.get("success", False)
        output = test_results.get("output", "")
        
        if success:
            sections.append("\n✅ **Tests PASSED**")
        else:
            sections.append("\n❌ **Tests FAILED**")
        
        if output:
            sections.append(f"\n```\n{output[:500]}\n```")
        
        return "\n".join(sections)
    
    def _generate_architectural_issues(self, analysis: GeminiAnalysis) -> str:
        """Generate architectural issues section"""
        sections = ["## 🏗️ Architectural Issues"]
        sections.append("\n*Issues that SonarQube's static analysis cannot detect*\n")
        
        if not analysis.parsed_data:
            return ""
        
        architectural_issues = analysis.parsed_data.get("architectural_issues", [])
        if not architectural_issues:
            return ""
        
        for arch in architectural_issues:
            severity_emoji = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡"}.get(arch.get("severity", "MEDIUM"), "⚪")
            sections.append(f"\n### {severity_emoji} {arch['title']}")
            sections.append(f"\n**Severity:** {arch.get('severity', 'MEDIUM')}")
            sections.append(f"\n**Description:** {arch['description']}")
            
            if arch.get("affected_components"):
                sections.append(f"\n**Affected Components:** {', '.join(arch['affected_components'])}")
            
            sections.append(f"\n**Consequences:** {arch.get('consequences', 'N/A')}")
            sections.append(f"\n**Recommended Pattern:** {arch.get('recommended_pattern', 'N/A')}")
            
            if arch.get("code_example"):
                sections.append("\n**Implementation Example:**\n```java\n" + arch['code_example'] + "\n```")
        
        return "\n".join(sections)
    
    def _generate_system_inconsistencies(self, analysis: GeminiAnalysis) -> str:
        """Generate system inconsistencies section"""
        sections = ["## ⚠️ System Inconsistencies"]
        sections.append("\n*Inconsistencies across the codebase that harm maintainability*\n")
        
        if not analysis.parsed_data:
            return ""
        
        inconsistencies = analysis.parsed_data.get("system_inconsistencies", [])
        if not inconsistencies:
            return ""
        
        for incons in inconsistencies:
            sections.append(f"\n### {incons['title']}")
            sections.append(f"\n**Type:** {incons.get('type', 'GENERAL')}")
            sections.append(f"\n**Description:** {incons['description']}")
            
            if incons.get("examples"):
                sections.append("\n**Examples:**")
                for ex in incons["examples"]:
                    sections.append(f"- {ex}")
            
            sections.append(f"\n**Impact:** {incons.get('impact', 'N/A')}")
            sections.append(f"\n**Fix Strategy:** {incons.get('fix_strategy', 'N/A')}")
            
            if incons.get("code_example"):
                sections.append("\n**Consistent Approach:**\n```java\n" + incons['code_example'] + "\n```")
        
        return "\n".join(sections)
    
    def _generate_security_deep_dive(self, analysis: GeminiAnalysis) -> str:
        """Generate security deep dive section"""
        sections = ["## 🔐 Advanced Security Analysis"]
        sections.append("\n*Security issues beyond SonarQube's detection capabilities*\n")
        
        if not analysis.parsed_data:
            return ""
        
        security_issues = analysis.parsed_data.get("security_deep_dive", [])
        if not security_issues:
            return ""
        
        for sec in security_issues:
            risk_emoji = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡"}.get(sec.get("risk_level", "MEDIUM"), "⚪")
            sections.append(f"\n### {risk_emoji} {sec['title']}")
            sections.append(f"\n**Why SonarQube Misses This:** {sec.get('beyond_sonarqube', 'N/A')}")
            sections.append(f"\n**Vulnerability Type:** {sec.get('vulnerability_type', 'N/A')}")
            sections.append(f"\n**Risk Level:** {sec.get('risk_level', 'MEDIUM')}")
            sections.append(f"\n**Attack Scenario:** {sec.get('attack_scenario', 'N/A')}")
            
            if sec.get("defensive_layers"):
                sections.append("\n**Defensive Layers:**")
                for layer in sec["defensive_layers"]:
                    sections.append(f"- {layer}")
            
            if sec.get("mitigation_code"):
                sections.append("\n**Secure Implementation:**\n```java\n" + sec['mitigation_code'] + "\n```")
        
        return "\n".join(sections)
    
    def _generate_performance_optimizations(self, analysis: GeminiAnalysis) -> str:
        """Generate performance optimizations section"""
        sections = ["## ⚡ Performance Optimizations"]
        sections.append("\n*Performance issues not detected by static analysis*\n")
        
        if not analysis.parsed_data:
            return ""
        
        perf_opts = analysis.parsed_data.get("performance_optimizations", [])
        if not perf_opts:
            return ""
        
        for perf in perf_opts:
            sections.append(f"\n### {perf['title']}")
            sections.append(f"\n**Current Problem:** {perf.get('current_problem', 'N/A')}")
            sections.append(f"\n**Impact:** {perf.get('impact', 'N/A')}")
            sections.append(f"\n**Strategy:** {perf.get('optimization_strategy', 'N/A')}")
            
            if perf.get("expected_improvement"):
                sections.append(f"\n**Expected Improvement:** {perf['expected_improvement']}")
            
            if perf.get("optimized_code"):
                sections.append("\n**Optimized Code:**\n```java\n" + perf['optimized_code'] + "\n```")
        
        return "\n".join(sections)
    
    def _generate_code_improvements(self, analysis: GeminiAnalysis) -> str:
        """Generate code improvements section"""
        sections = ["## 💡 Code Improvements"]
        sections.append("\n*Complete working code for major improvements*\n")
        
        if not analysis.parsed_data:
            return ""
        
        improvements = analysis.parsed_data.get("code_improvements", [])
        if not improvements:
            return ""
        
        for improvement in improvements:
            sections.append(f"\n### {improvement['title']}")
            sections.append(f"\n**Category:** {improvement.get('category', 'GENERAL')}")
            sections.append(f"\n**Current Approach:** {improvement.get('current_approach', 'N/A')}")
            
            if improvement.get("problems"):
                sections.append("\n**Problems:**")
                for prob in improvement["problems"]:
                    sections.append(f"- {prob}")
            
            sections.append(f"\n**Improved Approach:** {improvement.get('improved_approach', 'N/A')}")
            
            if improvement.get("benefits"):
                sections.append("\n**Benefits:**")
                for benefit in improvement["benefits"]:
                    sections.append(f"- ✅ {benefit}")
            
            if improvement.get("complete_code"):
                sections.append("\n**Complete Working Implementation:**\n```java\n" + improvement['complete_code'] + "\n```")
            
            if improvement.get("migration_steps"):
                sections.append("\n**Migration Steps:**")
                for i, step in enumerate(improvement["migration_steps"], 1):
                    sections.append(f"{i}. {step}")
        
        return "\n".join(sections)
    
    def _generate_best_practices_violations(self, analysis: GeminiAnalysis) -> str:
        """Generate best practices violations section"""
        sections = ["## 📚 Best Practices Violations"]
        
        if not analysis.parsed_data:
            return ""
        
        violations = analysis.parsed_data.get("best_practices_violations", [])
        if not violations:
            return ""
        
        for violation in violations:
            sections.append(f"\n### {violation.get('principle', 'General Principle')}")
            sections.append(f"\n**Violation:** {violation['violation_description']}")
            
            if violation.get("examples_from_code"):
                sections.append("\n**Examples from Code:**")
                for ex in violation["examples_from_code"]:
                    sections.append(f"- {ex}")
            
            sections.append(f"\n**Why It Matters:** {violation.get('why_it_matters', 'N/A')}")
            
            if violation.get("correct_implementation"):
                sections.append("\n**Correct Implementation:**\n```java\n" + violation['correct_implementation'] + "\n```")
        
        return "\n".join(sections)
    
    def _generate_sonarqube_gaps(self, analysis: GeminiAnalysis) -> str:
        """Generate SonarQube gaps section"""
        sections = ["## 🎯 Beyond SonarQube"]
        sections.append("\n*Critical findings that SonarQube cannot detect*\n")
        
        if not analysis.parsed_data:
            return ""
        
        gaps = analysis.parsed_data.get("sonarqube_gaps", [])
        if not gaps:
            return ""
        
        for gap in gaps:
            sections.append(f"\n### {gap['gap_type']}")
            sections.append(f"\n**Why Important:** {gap.get('why_important', 'N/A')}")
            sections.append(f"\n**Detection Method:** {gap.get('detection_method', 'Manual analysis')}")
            sections.append(f"\n**Remediation:** {gap.get('remediation', 'N/A')}")
            
            if gap.get("code_example"):
                sections.append("\n**Complete Solution:**\n```java\n" + gap['code_example'] + "\n```")
        
        return "\n".join(sections)
    
    def _generate_footer(self) -> str:
        """Generate report footer"""
        return """---

## 📝 Next Steps

1. **Review P0 Issues** - Address critical security and production risks immediately
2. **Plan P1 Issues** - Schedule critical technical debt resolution
3. **Validate Patches** - Review and test applied changes
4. **Monitor Metrics** - Track improvements in next SonarQube analysis

---

*Generated by Sonar AI Agent - Automated Code Quality Review*"""
