"""
Context extractor - retrieves code context for issues
"""

import os
from typing import List, Dict, Optional, Set
from dataclasses import dataclass
from ..sonar.models import Issue
from ..utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class CodeContext:
    """Code context for an issue"""
    file_path: str
    line_number: Optional[int]
    context_lines: List[str]
    start_line: int
    end_line: int
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "file_path": self.file_path,
            "line_number": self.line_number,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "context": "\n".join(self.context_lines),
        }


class ContextExtractor:
    """Extract code context around issues"""
    
    def __init__(self, repo_path: str, context_lines: int = 30):
        """
        Initialize context extractor
        
        Args:
            repo_path: Path to repository
            context_lines: Number of lines before/after issue line
        """
        self.repo_path = repo_path
        self.context_lines = context_lines
    
    def extract_file_content(self, file_path: str) -> Optional[List[str]]:
        """
        Read file content
        
        Args:
            file_path: Relative file path
        
        Returns:
            List of lines or None if file not found
        """
        full_path = os.path.join(self.repo_path, file_path)
        
        if not os.path.exists(full_path):
            logger.warning(f"File not found: {full_path}")
            return None
        
        try:
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.readlines()
        except Exception as e:
            logger.error(f"Error reading file {full_path}: {e}")
            return None
    
    def extract_context(self, issue: Issue, project_key: str) -> Optional[CodeContext]:
        """
        Extract code context for an issue
        
        Args:
            issue: Issue to extract context for
            project_key: SonarQube project key
        
        Returns:
            CodeContext or None if extraction fails
        """
        file_path = issue.get_file_path(project_key)
        line_number = issue.line
        
        if not line_number:
            logger.warning(f"No line number for issue {issue.key}")
            return None
        
        lines = self.extract_file_content(file_path)
        if not lines:
            return None
        
        # Calculate context window (1-indexed to 0-indexed)
        total_lines = len(lines)
        start_line = max(1, line_number - self.context_lines)
        end_line = min(total_lines, line_number + self.context_lines)
        
        # Extract context (convert to 0-indexed)
        context_lines = lines[start_line - 1:end_line]
        
        return CodeContext(
            file_path=file_path,
            line_number=line_number,
            context_lines=[line.rstrip("\n") for line in context_lines],
            start_line=start_line,
            end_line=end_line,
        )
    
    def extract_batch(
        self,
        issues: List[Issue],
        project_key: str,
        max_files: Optional[int] = None,
    ) -> Dict[str, CodeContext]:
        """
        Extract context for multiple issues
        
        Args:
            issues: List of issues
            project_key: SonarQube project key
            max_files: Maximum number of files to extract (limit scope)
        
        Returns:
            Dictionary mapping issue key to CodeContext
        """
        logger.info(f"Extracting code context for {len(issues)} issues...")
        
        contexts = {}
        processed_files: Set[str] = set()
        
        for issue in issues:
            file_path = issue.get_file_path(project_key)
            
            # Limit number of files if specified
            if max_files and len(processed_files) >= max_files:
                if file_path not in processed_files:
                    logger.info(f"Reached max files limit ({max_files}), skipping remaining")
                    break
            
            context = self.extract_context(issue, project_key)
            if context:
                contexts[issue.key] = context
                processed_files.add(file_path)
        
        logger.info(f"Extracted context for {len(contexts)} issues from {len(processed_files)} files")
        return contexts
