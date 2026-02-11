# Example Usage Guide

This guide shows you how to use Sonar AI Agent in different scenarios.

## Scenario 1: First Time Setup

```bash
# 1. Clone and navigate to project
cd sonar-ai-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure credentials
cp .env.example .env
# Edit .env with your credentials

# 4. Test with dry-run
python -m sonar_ai_agent.main run --dry-run --repo-path .
```

## Scenario 2: Analyze Java/Maven Project

```bash
# Ensure your project has pom.xml and SonarQube analysis done

# Set environment
export SONAR_HOST_URL=http://sonarqube.company.com
export SONAR_PROJECT_KEY=my-java-backend
export SONAR_TOKEN=sqp_abc123...
export GEMINI_API_KEY=AIza...

# Run analysis
python -m sonar_ai_agent.main run --repo-path /path/to/java/project

# Tests will run automatically after patching
```

## Scenario 3: Python Project Analysis

```bash
# For Python projects (no pom.xml)
# Tests won't run automatically, but patches will still be applied

python -m sonar_ai_agent.main run --repo-path /path/to/python/project
```

## Scenario 4: Review Only (No Patches)

```bash
# Just get the analysis and recommendations, don't apply patches
python -m sonar_ai_agent.main run --dry-run --repo-path .

# Check the report
cat sonar_ai_report.md
```

## Scenario 5: Custom Configuration

```bash
# Create a custom .env
cat > .env << EOF
SONAR_HOST_URL=http://localhost:9000
SONAR_PROJECT_KEY=my-project
SONAR_TOKEN=sqp_mytoken
GEMINI_API_KEY=AIza_mykey

# Customize limits
MAX_ISSUES=50          # Analyze more issues
MAX_FILES=10           # Process more files
MAX_CHANGED_LINES=300  # Allow more changes
EOF

# Run with custom config
python -m sonar_ai_agent.main run
```

## Scenario 6: CI/CD Integration (GitHub Actions)

Create `.github/workflows/sonar-analysis.yml`:

```yaml
name: Sonar AI Analysis

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday
  workflow_dispatch:      # Manual trigger

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install Sonar AI Agent
        run: |
          cd sonar-ai-agent
          pip install -r requirements.txt
      
      - name: Run Analysis (Dry-Run)
        env:
          SONAR_HOST_URL: ${{ secrets.SONAR_URL }}
          SONAR_PROJECT_KEY: ${{ secrets.SONAR_PROJECT }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          GEMINI_API_KEY: ${{ secrets.GEMINI_KEY }}
        run: |
          cd sonar-ai-agent
          python -m sonar_ai_agent.main run --dry-run --repo-path ..
      
      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: sonar-ai-report
          path: sonar-ai-agent/sonar_ai_report.md
```

## Scenario 7: Using from Python Script

```python
#!/usr/bin/env python3
"""
Custom script using Sonar AI Agent programmatically
"""

from sonar_ai_agent.config import Config
from sonar_ai_agent.main import SonarAIAgent
from sonar_ai_agent.utils.logger import setup_root_logger

# Setup logging
setup_root_logger()

# Configure
config = Config.from_env(
    dry_run=False,
    repo_path="/path/to/project"
)

# Run agent
agent = SonarAIAgent(config)
success = agent.run()

if success:
    print("✅ Analysis completed successfully!")
    
    # Read report
    with open("sonar_ai_report.md") as f:
        report = f.read()
    
    # Send to Slack, email, etc.
    # send_to_slack(report)
else:
    print("❌ Analysis failed")
```

## Scenario 8: Batch Analysis (Multiple Projects)

```python
#!/usr/bin/env python3
"""
Analyze multiple projects in batch
"""

import os
from sonar_ai_agent.config import Config
from sonar_ai_agent.main import SonarAIAgent

projects = [
    {"key": "backend-api", "path": "/projects/backend"},
    {"key": "frontend-app", "path": "/projects/frontend"},
    {"key": "mobile-app", "path": "/projects/mobile"},
]

for project in projects:
    print(f"\n{'='*60}")
    print(f"Analyzing: {project['key']}")
    print(f"{'='*60}")
    
    # Override project-specific config
    os.environ["SONAR_PROJECT_KEY"] = project["key"]
    
    config = Config.from_env(
        dry_run=True,
        repo_path=project["path"]
    )
    
    agent = SonarAIAgent(config)
    agent.run()
    
    # Rename report
    os.rename(
        "sonar_ai_report.md",
        f"reports/{project['key']}_report.md"
    )
```

## Scenario 9: Custom Triage Rules

```python
"""
Create custom triage logic for your organization
"""

from sonar_ai_agent.analyzer.triage import IssueTriage
from sonar_ai_agent.sonar.models import Issue, Priority

class MyCompanyTriage(IssueTriage):
    # Define your company's critical rules
    COMPANY_CRITICAL_RULES = [
        "java:S2259",  # Null pointer
        "java:S1313",  # IP address hardcoding
        # Add your critical rules
    ]
    
    @staticmethod
    def calculate_priority(issue: Issue) -> Priority:
        # Custom logic
        if issue.rule in MyCompanyTriage.COMPANY_CRITICAL_RULES:
            return Priority.P0
        
        # Fall back to default logic
        return IssueTriage.calculate_priority(issue)

# Use in your script
from sonar_ai_agent import config
from sonar_ai_agent.sonar.client import SonarQubeClient

config = Config.from_env()
client = SonarQubeClient(...)
data = client.fetch_all_data()

# Use custom triage
triaged = MyCompanyTriage.triage_issues(data.issues)
```

## Scenario 10: Generate Report Only

```bash
# If you already have sonar_bundle.json from previous run
# You can regenerate report without hitting APIs again

python3 << EOF
import json
from sonar_ai_agent.report.generator import ReportGenerator
from sonar_ai_agent.sonar.models import SonarData

# Load cached data
with open("sonar_bundle.json") as f:
    data = json.load(f)

# ... reconstruct objects ...

# Generate report
generator = ReportGenerator()
generator.generate(sonar_data, triaged_issues, analysis, [])
EOF
```

## Common Patterns

### Pattern 1: Progressive Analysis

```bash
# Start conservative
MAX_ISSUES=10 MAX_FILES=2 python -m sonar_ai_agent.main run --dry-run

# Review results, then increase
MAX_ISSUES=30 MAX_FILES=5 python -m sonar_ai_agent.main run --dry-run

# Finally apply
python -m sonar_ai_agent.main run
```

### Pattern 2: Security-First

```bash
# Analyze only P0 issues
# Modify config to filter only P0 after triage
# Apply patches only for security issues
```

### Pattern 3: Weekly Quality Check

```bash
# Add to crontab
0 9 * * 1 cd /path/to/sonar-ai-agent && python -m sonar_ai_agent.main run --dry-run && mail -s "Weekly Code Quality" team@company.com < sonar_ai_report.md
```

## Tips & Best Practices

1. **Always start with --dry-run**
2. **Commit your code before running in production mode**
3. **Review patches manually before merging**
4. **Set conservative limits initially**
5. **Use version control to track AI-generated changes**
6. **Run tests after applying patches**
7. **Keep API keys secure (never commit .env)**

## Troubleshooting Examples

### Issue: Too many changes

```bash
# Reduce limits
MAX_ISSUES=5 MAX_FILES=2 MAX_CHANGED_LINES=50 python -m sonar_ai_agent.main run --dry-run
```

### Issue: Gemini timeout

```python
# Add retry logic in gemini_client.py
# Or increase timeout in generation_config
```

### Issue: Patches fail to apply

```bash
# Check git status
git status

# Ensure clean working directory
git stash

# Try again
python -m sonar_ai_agent.main run
```

---

These examples cover most common use cases. Adapt them to your specific needs!
