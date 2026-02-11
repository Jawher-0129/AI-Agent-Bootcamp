"""
SonarQube API Client
"""

import requests
from typing import List, Dict, Any, Optional
from ..utils.logger import get_logger
from .models import Issue, QualityGate, Metrics, SonarData

logger = get_logger(__name__)


class SonarQubeClient:
    """Client for interacting with SonarQube API"""
    
    def __init__(self, host_url: str, token: str, project_key: str):
        self.host_url = host_url.rstrip("/")
        self.token = token
        self.project_key = project_key
        self.session = requests.Session()
        self.session.auth = (token, "")
        self.session.headers.update({"Accept": "application/json"})
    
    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GET request to SonarQube API"""
        url = f"{self.host_url}/api/{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"SonarQube API error: {e}")
            raise
    
    def get_quality_gate(self) -> QualityGate:
        """Fetch Quality Gate status"""
        logger.info("Fetching Quality Gate status...")
        data = self._get("qualitygates/project_status", {"projectKey": self.project_key})
        return QualityGate.from_dict(data)
    
    def get_metrics(self) -> Metrics:
        """Fetch project metrics"""
        logger.info("Fetching project metrics...")
        metric_keys = [
            "bugs",
            "vulnerabilities",
            "code_smells",
            "security_hotspots",
            "coverage",
            "duplicated_lines_density",
            "ncloc",
        ]
        
        params = {
            "component": self.project_key,
            "metricKeys": ",".join(metric_keys),
        }
        
        data = self._get("measures/component", params)
        measures = data.get("component", {}).get("measures", [])
        return Metrics.from_measures(measures)
    
    def get_issues(self, max_issues: int = 500) -> List[Issue]:
        """
        Fetch project issues with pagination
        
        Args:
            max_issues: Maximum number of issues to retrieve
        
        Returns:
            List of issues
        """
        logger.info("Fetching project issues...")
        all_issues = []
        page = 1
        page_size = 500
        
        while len(all_issues) < max_issues:
            params = {
                "componentKeys": self.project_key,
                "statuses": "OPEN,CONFIRMED,REOPENED",
                "p": page,
                "ps": min(page_size, max_issues - len(all_issues)),
            }
            
            data = self._get("issues/search", params)
            issues_data = data.get("issues", [])
            
            if not issues_data:
                break
            
            for issue_data in issues_data:
                all_issues.append(Issue.from_dict(issue_data))
            
            total = data.get("total", 0)
            logger.info(f"Retrieved {len(all_issues)} / {total} issues")
            
            if len(all_issues) >= total or len(all_issues) >= max_issues:
                break
            
            page += 1
        
        logger.info(f"Total issues retrieved: {len(all_issues)}")
        return all_issues
    
    def fetch_all_data(self, max_issues: int = 500) -> SonarData:
        """
        Fetch all SonarQube data (Quality Gate, Metrics, Issues)
        
        Args:
            max_issues: Maximum number of issues to retrieve
        
        Returns:
            Complete SonarData object
        """
        logger.info(f"Fetching SonarQube data for project: {self.project_key}")
        
        quality_gate = self.get_quality_gate()
        metrics = self.get_metrics()
        issues = self.get_issues(max_issues)
        
        return SonarData(
            quality_gate=quality_gate,
            metrics=metrics,
            issues=issues,
            project_key=self.project_key,
        )
