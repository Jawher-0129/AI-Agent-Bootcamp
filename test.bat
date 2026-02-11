@echo off
REM Quick test script for Sonar AI Agent on Windows

echo ============================================
echo    Sonar AI Agent - Quick Test
echo ============================================
echo.

REM Check if .env exists
if not exist ".env" (
    echo [!] Creating .env file...
    copy .env.example .env
    echo.
    echo [ACTION REQUIRED] Please edit .env with your credentials:
    echo   - SONAR_HOST_URL
    echo   - SONAR_PROJECT_KEY  
    echo   - SONAR_TOKEN
    echo   - GEMINI_API_KEY
    echo.
    notepad .env
    echo.
    echo Press any key after saving .env to continue...
    pause > nul
    echo.
)

echo [✓] .env file found
echo.

REM Verify Python
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo [✓] Python found
echo.

REM Check if main.py exists
if not exist "src\sonar_ai_agent\main.py" (
    echo [ERROR] main.py not found!
    echo Please run this script from the sonar-ai-agent directory
    pause
    exit /b 1
)

echo [✓] Source files found
echo.

echo ============================================
echo    Running Analysis (DRY-RUN mode)
echo ============================================
echo.
echo This will:
echo   1. Connect to SonarQube
echo   2. Fetch issues and metrics
echo   3. Analyze with Gemini AI
echo   4. Generate report
echo   5. NOT apply any patches (dry-run)
echo.
echo Press any key to start...
pause > nul
echo.

REM Run the agent
python run_agent.py run --dry-run --repo-path .

REM Check result
if errorlevel 1 (
    echo.
    echo ============================================
    echo    ❌ Test Failed
    echo ============================================
    echo.
    echo Common issues:
    echo   - Check .env file has correct values
    echo   - Verify SonarQube is accessible
    echo   - Verify Gemini API key is valid
    echo   - Check internet connection
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================
echo    ✅ Test Completed Successfully!
echo ============================================
echo.

REM Check if report exists
if exist "sonar_ai_report.md" (
    echo [✓] Report generated: sonar_ai_report.md
    echo.
    set /p open="Open report in Notepad? (y/n): "
    if /i "%open%"=="y" (
        notepad sonar_ai_report.md
    )
) else (
    echo [!] Report file not found (may have failed)
)

echo.
echo Files generated:
if exist "sonar_ai_report.md" echo   - sonar_ai_report.md
if exist "sonar_bundle.json" echo   - sonar_bundle.json
if exist "code_context.json" echo   - code_context.json
echo.

echo ============================================
echo    Next Steps
echo ============================================
echo.
echo 1. Review the report: sonar_ai_report.md
echo 2. If satisfied, run in production mode:
echo    python run_agent.py run
echo.
echo 3. Or use the interactive menu:
echo    run.bat
echo.
pause
