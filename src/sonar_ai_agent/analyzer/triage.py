"""
Intelligent triage and prioritization of SonarQube issues
"""

from typing import List, Dict
from ..sonar.models import Issue, Priority, IssueType, Severity
from ..utils.logger import get_logger

logger = get_logger(__name__)


class IssueTriage:
    """Intelligent issue prioritization"""
    
    # Security-related rules (P0)
    SECURITY_KEYWORDS = [
        "sql", "injection", "xss", "csrf", "auth", "password",
        "secret", "token", "vulnerability", "security", "insecure",
        "crypto", "encryption", "ldap", "xxe", "path-traversal",
    ]
    
    # Critical quality rules (P1)
    CRITICAL_KEYWORDS = [
        "null", "exception", "memory", "leak", "deadlock",
        "race-condition", "resource", "thread-safe", "concurrent",
    ]
    
    @staticmethod
    def calculate_priority(issue: Issue) -> Priority:
        """
        Calculate priority based on type, severity, and rule content
        
        Priority levels:
        - P0: Production/security risks (BLOCKER vulnerabilities, security issues)
        - P1: Critical technical debt (CRITICAL bugs, major code smells)
        - P2: Optimizations (other issues)
        """
        rule_lower = issue.rule.lower()
        message_lower = issue.message.lower()
        
        # P0: Critical security and production risks
        if issue.type == IssueType.VULNERABILITY:
            return Priority.P0
        
        if issue.type == IssueType.SECURITY_HOTSPOT:
            return Priority.P0
        
        if issue.severity == Severity.BLOCKER:
            return Priority.P0
        
        # Check for security keywords
        if any(keyword in rule_lower or keyword in message_lower 
               for keyword in IssueTriage.SECURITY_KEYWORDS):
            return Priority.P0
        
        # P1: Critical bugs and technical debt
        if issue.type == IssueType.BUG and issue.severity in [Severity.CRITICAL, Severity.MAJOR]:
            return Priority.P1
        
        if issue.severity == Severity.CRITICAL:
            return Priority.P1
        
        # Check for critical quality keywords
        if any(keyword in rule_lower or keyword in message_lower 
               for keyword in IssueTriage.CRITICAL_KEYWORDS):
            return Priority.P1
        
        # P2: Everything else (optimizations)
        return Priority.P2
    
    @staticmethod
    def triage_issues(issues: List[Issue]) -> Dict[Priority, List[Issue]]:
        """
        Triage and group issues by priority
        
        Args:
            issues: List of issues to triage
        
        Returns:
            Dictionary mapping Priority to list of issues
        """
        logger.info(f"Triaging {len(issues)} issues...")
        
        triaged = {
            Priority.P0: [],
            Priority.P1: [],
            Priority.P2: [],
        }
        
        for issue in issues:
            priority = IssueTriage.calculate_priority(issue)
            issue.priority = priority
            triaged[priority].append(issue)
        
        logger.info(f"P0: {len(triaged[Priority.P0])} | "
                   f"P1: {len(triaged[Priority.P1])} | "
                   f"P2: {len(triaged[Priority.P2])}")
        
        return triaged
    
    @staticmethod
    def select_top_issues(triaged: Dict[Priority, List[Issue]], max_issues: int) -> List[Issue]:
        """
        Select top issues respecting priority order
        
        Args:
            triaged: Dictionary of prioritized issues
            max_issues: Maximum number of issues to select
        
        Returns:
            List of top issues
        """
        selected = []
        
        # Select all P0, then P1, then P2
        for priority in [Priority.P0, Priority.P1, Priority.P2]:
            remaining = max_issues - len(selected)
            if remaining <= 0:
                break
            
            selected.extend(triaged[priority][:remaining])
        
        logger.info(f"Selected {len(selected)} top issues for analysis")
        return selected
