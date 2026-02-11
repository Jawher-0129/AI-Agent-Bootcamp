"""
SonarQube data models
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum


class Severity(str, Enum):
    """Issue severity levels"""
    BLOCKER = "BLOCKER"
    CRITICAL = "CRITICAL"
    MAJOR = "MAJOR"
    MINOR = "MINOR"
    INFO = "INFO"


class IssueType(str, Enum):
    """Issue types"""
    BUG = "BUG"
    VULNERABILITY = "VULNERABILITY"
    CODE_SMELL = "CODE_SMELL"
    SECURITY_HOTSPOT = "SECURITY_HOTSPOT"


class Priority(str, Enum):
    """Triage priority levels"""
    P0 = "P0"  # Critical: immediate production/security risks
    P1 = "P1"  # High: critical technical debt
    P2 = "P2"  # Medium: optimizations


@dataclass
class Issue:
    """SonarQube issue"""
    key: str
    rule: str
    severity: Severity
    type: IssueType
    message: str
    component: str
    line: Optional[int] = None
    status: str = "OPEN"
    effort: Optional[str] = None
    debt: Optional[str] = None
    
    # Computed fields
    priority: Optional[Priority] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Issue":
        """Create Issue from SonarQube API response"""
        return cls(
            key=data.get("key", ""),
            rule=data.get("rule", ""),
            severity=Severity(data.get("severity", "INFO")),
            type=IssueType(data.get("type", "CODE_SMELL")),
            message=data.get("message", ""),
            component=data.get("component", ""),
            line=data.get("line"),
            status=data.get("status", "OPEN"),
            effort=data.get("effort"),
            debt=data.get("debt"),
        )
    
    def get_file_path(self, project_key: str) -> str:
        """Extract file path from component"""
        # Component format: project:path/to/file.py
        if ":" in self.component:
            return self.component.split(":", 1)[1]
        return self.component


@dataclass
class QualityGate:
    """Quality Gate status"""
    status: str  # OK, WARN, ERROR
    conditions: List[Dict[str, Any]]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QualityGate":
        """Create QualityGate from API response"""
        project_status = data.get("projectStatus", {})
        return cls(
            status=project_status.get("status", "NONE"),
            conditions=project_status.get("conditions", []),
        )
    
    def is_passing(self) -> bool:
        """Check if quality gate is passing"""
        return self.status == "OK"


@dataclass
class Metrics:
    """Project metrics"""
    bugs: int = 0
    vulnerabilities: int = 0
    code_smells: int = 0
    security_hotspots: int = 0
    coverage: float = 0.0
    duplicated_lines_density: float = 0.0
    ncloc: int = 0
    
    @classmethod
    def from_measures(cls, measures: List[Dict[str, Any]]) -> "Metrics":
        """Create Metrics from SonarQube measures"""
        metrics_dict = {}
        for measure in measures:
            metric = measure.get("metric")
            value = measure.get("value", "0")
            
            if metric in ["bugs", "vulnerabilities", "code_smells", "security_hotspots", "ncloc"]:
                metrics_dict[metric] = int(float(value))
            elif metric in ["coverage", "duplicated_lines_density"]:
                metrics_dict[metric] = float(value)
        
        return cls(**metrics_dict)


@dataclass
class SonarData:
    """Complete SonarQube analysis data"""
    quality_gate: QualityGate
    metrics: Metrics
    issues: List[Issue]
    project_key: str
    
    def get_critical_issues(self) -> List[Issue]:
        """Get critical issues (BLOCKER, CRITICAL, BUG, VULNERABILITY)"""
        return [
            issue for issue in self.issues
            if issue.severity in [Severity.BLOCKER, Severity.CRITICAL]
            or issue.type in [IssueType.BUG, IssueType.VULNERABILITY]
        ]
