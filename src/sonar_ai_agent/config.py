"""
Configuration management and validation for Sonar AI Agent
"""

import os
import sys
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv


@dataclass
class Config:
    """Application configuration with security and limits"""
    
    # Required SonarQube settings
    sonar_host_url: str
    sonar_project_key: str
    sonar_token: str
    
    # Required Gemini settings
    gemini_api_key: str
    gemini_model: str = "gemini-flash-latest"
    
    # Safety limits
    max_issues: int = 30
    max_files: int = 5
    max_changed_lines: int = 200
    
    # Runtime options
    dry_run: bool = False
    repo_path: str = "."
    
    @classmethod
    def from_env(cls, dry_run: bool = False, repo_path: str = ".") -> "Config":
        """
        Load configuration from environment variables.
        Exits immediately if required variables are missing.
        """
        load_dotenv()
        
        # Validate required environment variables
        required_vars = {
            "SONAR_HOST_URL": os.getenv("SONAR_HOST_URL"),
            "SONAR_PROJECT_KEY": os.getenv("SONAR_PROJECT_KEY"),
            "SONAR_TOKEN": os.getenv("SONAR_TOKEN"),
            "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
        }
        
        missing_vars = [key for key, value in required_vars.items() if not value]
        
        if missing_vars:
            print("❌ ERROR: Missing required environment variables:")
            for var in missing_vars:
                print(f"  - {var}")
            print("\n💡 Please set these variables in .env file or environment.")
            print("   See .env.example for reference.")
            sys.exit(1)
        
        # Optional limits with defaults
        max_issues = int(os.getenv("MAX_ISSUES", "30"))
        max_files = int(os.getenv("MAX_FILES", "5"))
        max_changed_lines = int(os.getenv("MAX_CHANGED_LINES", "200"))
        gemini_model = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
        
        return cls(
            sonar_host_url=required_vars["SONAR_HOST_URL"].rstrip("/"),
            sonar_project_key=required_vars["SONAR_PROJECT_KEY"],
            sonar_token=required_vars["SONAR_TOKEN"],
            gemini_api_key=required_vars["GEMINI_API_KEY"],
            gemini_model=gemini_model,
            max_issues=max_issues,
            max_files=max_files,
            max_changed_lines=max_changed_lines,
            dry_run=dry_run,
            repo_path=repo_path,
        )
    
    def validate(self) -> None:
        """Validate configuration values"""
        if self.max_issues <= 0:
            raise ValueError("max_issues must be positive")
        if self.max_files <= 0:
            raise ValueError("max_files must be positive")
        if self.max_changed_lines <= 0:
            raise ValueError("max_changed_lines must be positive")
        if not os.path.exists(self.repo_path):
            raise ValueError(f"Repository path does not exist: {self.repo_path}")
