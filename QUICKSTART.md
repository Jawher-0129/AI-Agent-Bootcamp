# Sonar AI Agent - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
SONAR_HOST_URL=http://your-sonarqube-url
SONAR_PROJECT_KEY=your-project-key
SONAR_TOKEN=your-sonar-token
GEMINI_API_KEY=your-gemini-api-key
```

### Step 3: Run in Dry-Run Mode

Test without applying changes:

```bash
python run_agent.py run --dry-run
```

### Step 4: Review Output

Check the generated files:
- `sonar_ai_report.md` - Full analysis report
- `sonar_bundle.json` - SonarQube data
- `code_context.json` - Code contexts

### Step 5: Apply Patches (Optional)

If you're satisfied with the dry-run results:

```bash
python run_agent.py run
```

## 📊 What You'll Get

1. **Intelligent Triage**: Issues automatically prioritized as P0/P1/P2
2. **AI Analysis**: Gemini provides expert-level code review
3. **Root Cause Analysis**: Issues grouped by underlying problems
4. **Actionable Recommendations**: Specific improvements with measurable benefits
5. **Safe Patches**: Validated, minimal code changes
6. **Test Verification**: Automatic Maven test execution
7. **Professional Report**: Markdown report ready to share

## 🛡️ Safety First

- Start with `--dry-run` to preview changes
- Review patches before applying
- Patches are limited by safety rules
- Tests run automatically after patching

## 🆘 Need Help?

Common issues:

**Missing environment variables:**
```bash
# Make sure .env file exists and contains all required variables
cat .env
```

**SonarQube connection issues:**
```bash
# Test your SonarQube URL
curl -u YOUR_TOKEN: http://your-sonarqube/api/system/status
```

**Gemini API issues:**
- Check API key is valid
- Verify you have API quota remaining
- Ensure internet connectivity

## 📚 Next Steps

1. Read the full [README.md](README.md)
2. Customize triage rules in `analyzer/triage.py`
3. Adjust safety limits in `.env`
4. Integrate into CI/CD pipeline

---

Happy analyzing! 🎯
