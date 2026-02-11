# 🤖 Sonar AI Agent

**Automated Code Quality Review with AI**

An ultra-intelligent Python agent that analyzes SonarQube results, prioritizes issues with smart triage, and leverages Gemini AI to provide expert code review, root cause analysis, and automated safe patches.

## ✨ Features

- 🔍 **Intelligent Issue Triage** - Automatic P0/P1/P2 prioritization based on severity, type, and security impact
- 🧠 **AI-Powered Analysis** - Uses Google Gemini to provide senior engineer-level code review
- 📊 **Comprehensive Reporting** - Professional Markdown reports with actionable insights
- 🔧 **Safe Auto-Patching** - Validates and applies only safe, minimal code changes
- 🧪 **Maven Test Integration** - Automatically runs tests after applying patches
- 🛡️ **Security-First** - No hardcoded secrets, configurable limits, extensive validation

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Git
- SonarQube instance with API access
- Google Gemini API key

### Installation

1. Clone the repository:
```bash
cd sonar-ai-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your actual credentials
```

Required environment variables:
- `SONAR_HOST_URL` - Your SonarQube server URL
- `SONAR_PROJECT_KEY` - Project key in SonarQube
- `SONAR_TOKEN` - SonarQube authentication token
- `GEMINI_API_KEY` - Google Gemini API key

Optional configuration:
- `MAX_ISSUES=30` - Maximum issues to analyze
- `MAX_FILES=5` - Maximum files to process
- `MAX_CHANGED_LINES=200` - Maximum lines changed per run

### Usage

**Windows (recommended method):**
```powershell
# Direct execution (no installation needed)
python run_agent.py run --dry-run --repo-path .

# Or use the helper script
.\run.bat
```

**Linux/Mac:**
```bash
# Option 1: Install package first
pip install -e .
python -m sonar_ai_agent.main run --dry-run

# Option 2: Direct execution
python run_agent.py run --dry-run
```

**Dry run (no changes applied):**
```bash
python run_agent.py run --repo-path . --dry-run
```

**Production run (applies patches):**
```bash
python run_agent.py run --repo-path .
```

**For a different repository:**
```bash
python run_agent.py run --repo-path /path/to/your/repo
```

> 📝 **Windows Users**: See [WINDOWS_GUIDE.md](WINDOWS_GUIDE.md) for detailed Windows-specific instructions

## 📁 Project Structure

```
sonar-ai-agent/
├── src/
│   └── sonar_ai_agent/
│       ├── __init__.py
│       ├── main.py              # Entry point
│       ├── config.py            # Configuration management
│       ├── sonar/               # SonarQube integration
│       │   ├── client.py        # API client
│       │   └── models.py        # Data models
│       ├── analyzer/            # Analysis engine
│       │   ├── triage.py        # Issue prioritization
│       │   ├── context_extractor.py  # Code context extraction
│       │   └── gemini_client.py      # Gemini AI integration
│       ├── patcher/             # Patch system
│       │   ├── patch_validator.py    # Patch validation
│       │   └── patch_applier.py      # Patch application
│       ├── report/              # Report generation
│       │   └── generator.py     # Markdown report generator
│       └── utils/               # Utilities
│           └── logger.py        # Logging
├── requirements.txt
├── .env.example
└── README.md
```

## 🎯 How It Works

### 1. Data Collection
- Fetches Quality Gate status from SonarQube
- Retrieves project metrics (bugs, vulnerabilities, coverage, etc.)
- Collects all open issues with details

### 2. Intelligent Triage
Issues are automatically prioritized:
- **P0 (Critical)**: Security vulnerabilities, blockers, production risks
- **P1 (High)**: Critical bugs, major technical debt
- **P2 (Medium)**: Code smells, minor improvements

### 3. Context Extraction
- Extracts ±30 lines of code context around each issue
- Respects file limits to prevent over-processing
- Saves context for AI analysis

### 4. AI Analysis with Gemini
Gemini provides:
- **Executive Summary**: High-level code quality assessment
- **Root Cause Analysis**: Groups issues by underlying problems
- **Expert Recommendations**: Actionable improvements with measurable benefits
- **Optimizations**: Quick wins, safe refactors, strategic improvements
- **Safe Patches**: Minimal, validated code changes

### 5. Patch Validation & Application
- Validates patch format and safety
- Rejects patches that:
  - Change public APIs
  - Modify function signatures
  - Include dangerous operations
  - Exceed line change limits
- Applies valid patches using `git apply`

### 6. Test Verification
- Automatically detects Maven projects
- Runs `mvn test` after applying patches
- Reports test results in final report

### 7. Report Generation
Creates `sonar_ai_report.md` with:
- Executive summary
- Health snapshot with metrics
- Prioritized issue triage
- Root cause analysis
- Actionable recommendations
- Optimization suggestions
- Patch application summary
- Test verification results

## 🛡️ Safety Features

### Strict Limits
- Maximum issues analyzed (default: 30)
- Maximum files processed (default: 5)
- Maximum lines changed (default: 200)

### Patch Safety Rules
- No class definition changes
- No function signature modifications
- No public API changes
- No decorator changes
- No import modifications
- No destructive operations

### Validation
- JSON schema validation for Gemini responses
- Unified diff format validation
- Git apply dry-run before actual application
- Configurable dry-run mode for testing

## 📊 Output Files

After running, you'll get:

1. **sonar_ai_report.md** - Comprehensive Markdown report
2. **sonar_bundle.json** - Raw SonarQube data
3. **code_context.json** - Extracted code contexts

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Required
SONAR_HOST_URL=http://localhost:9000
SONAR_PROJECT_KEY=my-project
SONAR_TOKEN=sqp_your_token_here
GEMINI_API_KEY=your_gemini_key_here

# Optional (with defaults)
MAX_ISSUES=30
MAX_FILES=5
MAX_CHANGED_LINES=200
```

### Getting API Keys

**SonarQube Token:**
1. Login to SonarQube
2. Go to: User Menu → My Account → Security
3. Generate new token

**Gemini API Key:**
1. Visit: https://makersuite.google.com/app/apikey
2. Create new API key
3. Copy to `.env`

## 🐛 Troubleshooting

### "Missing required environment variables"
- Ensure `.env` file exists and contains all required variables
- Check that variables are not empty

### "git not found - cannot apply patches"
- Ensure Git is installed and in PATH
- Patches require Git for `git apply` command

### "SonarQube API error"
- Verify `SONAR_HOST_URL` is correct and reachable
- Check `SONAR_TOKEN` is valid
- Ensure project key exists in SonarQube

### "Gemini API error"
- Verify API key is valid
- Check API quotas/limits
- Ensure internet connectivity

## 🚀 Advanced Usage

### Custom Repository Path
```bash
python -m sonar_ai_agent.main run --repo-path /path/to/project
```

### Dry Run (No Changes)
```bash
python -m sonar_ai_agent.main run --dry-run
```

### From Python Code
```python
from sonar_ai_agent.config import Config
from sonar_ai_agent.main import SonarAIAgent

config = Config.from_env(dry_run=True, repo_path=".")
agent = SonarAIAgent(config)
agent.run()
```

## 📝 Requirements

- Python 3.8+
- `requests` - HTTP client
- `google-generativeai` - Gemini AI
- `python-dotenv` - Environment variables
- `pydantic` - Data validation

## 🤝 Contributing

This is a production-ready template for AI-powered code quality analysis. Feel free to:
- Add support for other code quality platforms (CodeClimate, etc.)
- Integrate with other LLMs (OpenAI, Anthropic, etc.)
- Enhance patch generation logic
- Add more triage intelligence

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Credits

Built with ❤️ for AI-Agent Bootcamp

---

**Note:** Always review patches before deploying to production. While the agent uses extensive safety checks, human review ensures changes align with your project's specific requirements.
