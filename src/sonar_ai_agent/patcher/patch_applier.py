"""
Patch applier - applies validated patches to repository
"""

import os
import subprocess
import tempfile
from typing import List, Dict, Optional
from dataclasses import dataclass
from ..utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class PatchResult:
    """Result of patch application"""
    success: bool
    file_path: str
    message: str
    error: Optional[str] = None


class PatchApplier:
    """Applies patches to repository"""
    
    def __init__(self, repo_path: str, dry_run: bool = False):
        """
        Initialize patch applier
        
        Args:
            repo_path: Path to repository
            dry_run: If True, don't actually apply patches
        """
        self.repo_path = repo_path
        self.dry_run = dry_run
    
    def apply_patch(self, patch: Dict) -> PatchResult:
        """
        Apply a single patch
        
        Args:
            patch: Patch dictionary with file_path and diff
        
        Returns:
            PatchResult
        """
        file_path = patch.get("file_path", "")
        diff = patch.get("diff", "")
        issue_key = patch.get("issue_key", "unknown")
        
        if self.dry_run:
            logger.info(f"[DRY RUN] Would apply patch for {file_path} (issue: {issue_key})")
            return PatchResult(
                success=True,
                file_path=file_path,
                message=f"Dry run - patch for {issue_key}"
            )
        
        try:
            # Create temporary patch file
            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".patch",
                delete=False,
                encoding="utf-8"
            ) as tmp_file:
                tmp_file.write(diff)
                tmp_patch_path = tmp_file.name
            
            # Apply patch using 'patch' command (Unix) or 'git apply' (cross-platform)
            success = self._apply_with_git(tmp_patch_path)
            
            # Clean up temp file
            os.unlink(tmp_patch_path)
            
            if success:
                logger.info(f"✓ Successfully applied patch for {file_path}")
                return PatchResult(
                    success=True,
                    file_path=file_path,
                    message=f"Applied patch for issue {issue_key}"
                )
            else:
                logger.error(f"✗ Failed to apply patch for {file_path}")
                return PatchResult(
                    success=False,
                    file_path=file_path,
                    message=f"Failed to apply patch for issue {issue_key}",
                    error="Patch command failed"
                )
        
        except Exception as e:
            logger.error(f"Error applying patch for {file_path}: {e}")
            return PatchResult(
                success=False,
                file_path=file_path,
                message=f"Exception applying patch for issue {issue_key}",
                error=str(e)
            )
    
    def _apply_with_git(self, patch_path: str) -> bool:
        """
        Apply patch using git apply
        
        Args:
            patch_path: Path to patch file
        
        Returns:
            True if successful
        """
        try:
            result = subprocess.run(
                ["git", "apply", "--whitespace=fix", patch_path],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=30,
            )
            
            if result.returncode == 0:
                return True
            
            logger.warning(f"git apply failed: {result.stderr}")
            
            # Try with --reject to create .rej files for failed hunks
            result = subprocess.run(
                ["git", "apply", "--reject", "--whitespace=fix", patch_path],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=30,
            )
            
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            logger.error("git apply timed out")
            return False
        except FileNotFoundError:
            logger.error("git not found - cannot apply patches")
            return False
        except Exception as e:
            logger.error(f"Error running git apply: {e}")
            return False
    
    def apply_batch(self, patches: List[Dict]) -> List[PatchResult]:
        """
        Apply multiple patches
        
        Args:
            patches: List of patch dictionaries
        
        Returns:
            List of PatchResults
        """
        if not patches:
            logger.info("No patches to apply")
            return []
        
        logger.info(f"Applying {len(patches)} patches...")
        
        results = []
        for i, patch in enumerate(patches, 1):
            logger.info(f"Applying patch {i}/{len(patches)}...")
            result = self.apply_patch(patch)
            results.append(result)
        
        successes = sum(1 for r in results if r.success)
        logger.info(f"Applied {successes}/{len(patches)} patches successfully")
        
        return results
