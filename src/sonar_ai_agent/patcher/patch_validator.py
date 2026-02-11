"""
Patch validator - ensures patches are safe to apply
"""

import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from ..utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class ValidationResult:
    """Result of patch validation"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    
    def __bool__(self):
        return self.is_valid


class PatchValidator:
    """Validates patches for safety"""
    
    # Dangerous patterns that should not be auto-patched
    DANGEROUS_PATTERNS = [
        r"class\s+\w+",  # Class definition changes
        r"def\s+\w+\s*\(",  # Function signature changes
        r"public\s+\w+",  # Public API changes
        r"@\w+",  # Decorator changes
        r"import\s+",  # Import changes
        r"from\s+\w+\s+import",  # Import changes
    ]
    
    # Unsafe keywords
    UNSAFE_KEYWORDS = [
        "delete",
        "drop",
        "truncate",
        "remove_all",
        "destroy",
    ]
    
    def __init__(self, max_changed_lines: int = 200):
        """
        Initialize validator
        
        Args:
            max_changed_lines: Maximum number of changed lines allowed
        """
        self.max_changed_lines = max_changed_lines
    
    def validate_diff(self, diff: str, file_path: str) -> ValidationResult:
        """
        Validate a unified diff
        
        Args:
            diff: Unified diff string
            file_path: Path to file being patched
        
        Returns:
            ValidationResult
        """
        errors = []
        warnings = []
        
        # Check if diff is empty
        if not diff or not diff.strip():
            errors.append("Empty diff")
            return ValidationResult(False, errors, warnings)
        
        # Parse diff and count changes
        changed_lines = self._count_changed_lines(diff)
        
        if changed_lines > self.max_changed_lines:
            errors.append(
                f"Too many changes: {changed_lines} lines "
                f"(max: {self.max_changed_lines})"
            )
        
        # Check for dangerous patterns
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, diff, re.MULTILINE):
                warnings.append(f"Contains potentially dangerous pattern: {pattern}")
        
        # Check for unsafe keywords
        diff_lower = diff.lower()
        for keyword in self.UNSAFE_KEYWORDS:
            if keyword in diff_lower:
                errors.append(f"Contains unsafe keyword: {keyword}")
        
        # Check for valid unified diff format
        if not self._is_valid_unified_diff(diff):
            errors.append("Invalid unified diff format")
        
        is_valid = len(errors) == 0
        
        if is_valid:
            logger.info(f"✓ Patch validation passed for {file_path}")
        else:
            logger.warning(f"✗ Patch validation failed for {file_path}: {errors}")
        
        return ValidationResult(is_valid, errors, warnings)
    
    def _count_changed_lines(self, diff: str) -> int:
        """Count number of changed lines in diff"""
        count = 0
        for line in diff.split("\n"):
            if line.startswith("+") and not line.startswith("+++"):
                count += 1
            elif line.startswith("-") and not line.startswith("---"):
                count += 1
        return count
    
    def _is_valid_unified_diff(self, diff: str) -> bool:
        """Check if diff is in valid unified diff format"""
        lines = diff.split("\n")
        
        # Must have file headers
        has_from = any(line.startswith("---") for line in lines)
        has_to = any(line.startswith("+++") for line in lines)
        has_hunk = any(line.startswith("@@") for line in lines)
        
        return has_from and has_to and has_hunk
    
    def validate_batch(self, patches: List[Dict]) -> List[Dict]:
        """
        Validate multiple patches and filter out invalid ones
        
        Args:
            patches: List of patch dictionaries
        
        Returns:
            List of valid patches
        """
        valid_patches = []
        
        for patch in patches:
            file_path = patch.get("file_path", "unknown")
            diff = patch.get("diff", "")
            
            result = self.validate_diff(diff, file_path)
            
            if result.is_valid:
                valid_patches.append(patch)
                if result.warnings:
                    logger.warning(f"Warnings for {file_path}: {result.warnings}")
            else:
                logger.warning(f"Skipping invalid patch for {file_path}: {result.errors}")
        
        logger.info(f"Validated {len(valid_patches)}/{len(patches)} patches")
        return valid_patches
