# Sonar AI Agent - Architecture Overview

## 🏗️ Architecture

Sonar AI Agent follows a modular, production-ready architecture:

```
┌─────────────────────────────────────────────────────────┐
│                    Main Orchestrator                    │
│                  (main.py)                             │
└────────────┬────────────────────────────────────────────┘
             │
             ├─► 1. SonarQube Client
             │    └─► Fetch: Quality Gate, Metrics, Issues
             │
             ├─► 2. Issue Triage
             │    └─► Prioritize: P0 (Critical) → P1 (High) → P2 (Medium)
             │
             ├─► 3. Context Extractor
             │    └─► Extract code context (±30 lines per issue)
             │
             ├─► 4. Gemini AI Client
             │    └─► Analyze: Root causes, recommendations, patches
             │
             ├─► 5. Patch Validator
             │    └─► Validate: Safety rules, format, limits
             │
             ├─► 6. Patch Applier
             │    └─► Apply: Git apply with safety checks
             │
             ├─► 7. Test Runner
             │    └─► Execute: Maven tests (if applicable)
             │
             └─► 8. Report Generator
                  └─► Generate: Professional Markdown report
```

## 📦 Module Breakdown

### 1. Configuration (`config.py`)
- Environment variable validation
- Security-first approach (no hardcoded secrets)
- Fail-fast on missing required config
- Configurable safety limits

### 2. SonarQube Integration (`sonar/`)
- **client.py**: REST API client with pagination
- **models.py**: Type-safe data models
  - `Issue`: Represents a SonarQube issue
  - `QualityGate`: Quality gate status
  - `Metrics`: Project metrics
  - `SonarData`: Complete analysis data

### 3. Analyzer (`analyzer/`)
- **triage.py**: Intelligent prioritization
  - Security-focused P0 detection
  - Critical bug identification
  - Pattern-based classification
- **context_extractor.py**: Code context extraction
  - File reading with encoding handling
  - Context window management (±N lines)
  - Multi-file support with limits
- **gemini_client.py**: AI analysis
  - Structured prompt engineering
  - JSON schema validation
  - Error handling and retry logic

### 4. Patcher (`patcher/`)
- **patch_validator.py**: Safety validation
  - Dangerous pattern detection
  - Line change limits
  - Unified diff format validation
- **patch_applier.py**: Safe application
  - Git apply integration
  - Dry-run support
  - Atomic operations
  - Rollback capability

### 5. Report Generator (`report/`)
- **generator.py**: Markdown report creation
  - Executive summary
  - Health metrics with scoring
  - Prioritized triage view
  - Root cause mapping
  - Actionable recommendations
  - Patch summary
  - Test results

### 6. Utils (`utils/`)
- **logger.py**: Consistent logging
  - Structured logging format
  - Multiple log levels
  - Color-coded output (optional)

## 🔄 Data Flow

```
Environment Variables
        ↓
    Config Validation
        ↓
┌───────────────────────┐
│  SonarQube API Call   │
│  - Quality Gate       │
│  - Metrics            │
│  - Issues (paginated) │
└───────────┬───────────┘
            │
            ↓
    ┌───────────────┐
    │ Issue Triage  │
    │ P0 / P1 / P2  │
    └───────┬───────┘
            │
            ↓
    ┌────────────────────┐
    │ Context Extraction │
    │ ±30 lines per issue│
    └────────┬───────────┘
             │
             ↓
    ┌─────────────────────┐
    │   Gemini AI Call    │
    │  (Structured JSON)  │
    └─────────┬───────────┘
              │
              ↓
      ┌───────────────┐
      │ Parse Response│
      │  - Triage     │
      │  - Root Causes│
      │  - Recs       │
      │  - Patches    │
      └───────┬───────┘
              │
              ↓
      ┌─────────────────┐
      │ Patch Validation│
      │ (Safety Checks) │
      └────────┬────────┘
               │
               ↓
        ┌──────────────┐
        │ Apply Patches│
        │   (Git)      │
        └──────┬───────┘
               │
               ↓
        ┌─────────────┐
        │  Run Tests  │
        │   (Maven)   │
        └──────┬──────┘
               │
               ↓
     ┌──────────────────┐
     │ Generate Report  │
     │   (Markdown)     │
     └──────────────────┘
```

## 🔐 Security Design

### 1. No Hardcoded Secrets
- All credentials via environment variables
- `.env` file not committed to Git
- Fail-fast on missing credentials

### 2. Patch Safety
- Maximum lines changed limit
- Dangerous pattern detection
- No API-breaking changes
- No destructive operations
- Git-based application (atomic)

### 3. Validation Layers
```
Gemini Output
     ↓
JSON Schema Validation
     ↓
Patch Format Validation
     ↓
Safety Pattern Check
     ↓
Line Limit Check
     ↓
Dry-Run Capability
     ↓
Git Apply (with --reject)
```

## 🎯 Design Principles

1. **Modularity**: Each component has single responsibility
2. **Type Safety**: Dataclasses for structured data
3. **Error Handling**: Graceful failures with clear messages
4. **Logging**: Comprehensive logging at all stages
5. **Configurability**: Adjustable limits and thresholds
6. **Safety**: Multiple validation layers
7. **Testability**: Pure functions, dependency injection
8. **Cross-Platform**: Windows/Linux/Mac compatible

## 🔧 Extension Points

### Add New Issue Source
Implement similar to `sonar/client.py`:
```python
class CodeClimateClient:
    def fetch_all_data(self) -> SonarData:
        # Transform to common format
        pass
```

### Add New LLM Provider
Implement similar to `analyzer/gemini_client.py`:
```python
class OpenAIClient:
    def analyze(self, data) -> Analysis:
        # Use OpenAI API
        pass
```

### Custom Triage Logic
Extend `analyzer/triage.py`:
```python
class CustomTriage(IssueTriage):
    @staticmethod
    def calculate_priority(issue: Issue) -> Priority:
        # Custom logic
        pass
```

### Custom Report Format
Extend `report/generator.py`:
```python
class JSONReportGenerator(ReportGenerator):
    def generate(self, data) -> str:
        # Generate JSON instead of Markdown
        pass
```

## 📊 Performance Considerations

- **Pagination**: Handles large issue sets efficiently
- **Rate Limiting**: Can add rate limiting for API calls
- **Parallel Processing**: Can parallelize context extraction
- **Caching**: Can cache SonarQube responses
- **Streaming**: Can stream Gemini responses for large analyses

## 🧪 Testing Strategy

```
Unit Tests
├── Config validation
├── Issue triage logic
├── Patch validation rules
└── Report formatting

Integration Tests
├── SonarQube API calls (mocked)
├── Gemini API calls (mocked)
└── Git apply operations

End-to-End Tests
└── Full workflow with test project
```

## 📈 Future Enhancements

- [ ] Support for multiple code quality platforms
- [ ] Multi-LLM fallback (OpenAI, Anthropic, Azure)
- [ ] Patch preview UI
- [ ] CI/CD integration templates
- [ ] Slack/Teams notifications
- [ ] Historical trend analysis
- [ ] Custom rule definitions
- [ ] Plugin system for extensibility

---

This architecture ensures the agent is production-ready, maintainable, and extensible.
