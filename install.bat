@echo off
REM Quick install script for Sonar AI Agent

echo ============================================
echo    Sonar AI Agent - Quick Install
echo ============================================
echo.

echo [1/2] Installing package in editable mode...
python -m pip install -e .

if errorlevel 1 (
    echo.
    echo [ERROR] Installation failed!
    echo.
    echo Try: python -m pip install --upgrade pip
    pause
    exit /b 1
)

echo.
echo [2/2] Checking installation...
python -c "import sonar_ai_agent; print('✓ Package installed successfully!')"

if errorlevel 1 (
    echo [ERROR] Package not found after installation
    pause
    exit /b 1
)

echo.
echo ============================================
echo    ✓ Installation Complete!
echo ============================================
echo.
echo You can now run:
echo   1. python src\sonar_ai_agent\main.py run --dry-run
echo   2. Or use: .\run.bat
echo.
pause
