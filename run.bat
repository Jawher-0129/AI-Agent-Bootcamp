@echo off
REM Sonar AI Agent - Windows Helper Script

echo ============================================
echo    Sonar AI Agent - Windows Setup
echo ============================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check if .env exists
if not exist ".env" (
    echo [INFO] Creating .env from template...
    copy .env.example .env
    echo [ACTION REQUIRED] Please edit .env with your credentials
    echo Opening .env in notepad...
    notepad .env
    echo.
)

echo ============================================
echo    Choose an option:
echo ============================================
echo 1. Install dependencies
echo 2. Run dry-run (test mode)
echo 3. Run production (apply patches)
echo 4. View last report
echo 5. Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto install
if "%choice%"=="2" goto dryrun
if "%choice%"=="3" goto production
if "%choice%"=="4" goto report
if "%choice%"=="5" goto end

echo Invalid choice!
pause
exit /b 1

:install
echo.
echo Installing dependencies...
python -m pip install -e .
if errorlevel 1 (
    echo [ERROR] Installation failed!
    pause
    exit /b 1
)
echo.
echo [SUCCESS] Dependencies installed!
echo [INFO] You can now use 'sonar-ai-agent' command directly!
pause
goto end

:dryrun
echo.
echo Running in DRY-RUN mode (no changes will be applied)...
echo.
python run_agent.py run --dry-run
echo.
echo [DONE] Check sonar_ai_report.md for results
pause
goto end

:production
echo.
echo ============================================
echo    WARNING: PRODUCTION MODE
echo ============================================
echo This will apply patches to your code!
echo Make sure you have:
echo   1. Reviewed the dry-run results
echo   2. Committed your current changes
echo   3. Backed up your code
echo.
set /p confirm="Are you sure? (yes/no): "
if not "%confirm%"=="yes" (
    echo Cancelled.
    pause
    goto end
)
echo.
echo Running in PRODUCTION mode...
echo.
python run_agent.py run
echo.
echo [DONE] Check sonar_ai_report.md for results
pause
goto end

:report
echo.
if exist "sonar_ai_report.md" (
    echo Opening report...
    start sonar_ai_report.md
) else (
    echo [ERROR] No report found. Run the agent first!
)
pause
goto end

:end
echo.
echo Goodbye!
