"""
Setup script for Sonar AI Agent
"""

from setuptools import setup, find_packages

setup(
    name="sonar-ai-agent",
    version="1.0.0",
    description="Automated Code Quality Review with AI",
    author="AI-Agent Bootcamp",
    python_requires=">=3.8",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "requests>=2.31.0",
        "google-generativeai>=0.3.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.0",
    ],
    entry_points={
        "console_scripts": [
            "sonar-ai-agent=sonar_ai_agent.main:main",
        ],
    },
)
