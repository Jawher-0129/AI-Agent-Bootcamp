@echo off
REM Helper to find Java project path

echo ============================================
echo    Find Java Project Path
echo ============================================
echo.

echo Searching for Java projects in parent directories...
echo.

REM Check common locations
set FOUND=0

REM Check parent directory
if exist "..\PaiementManagement" (
    echo [FOUND] ..\PaiementManagement
    set FOUND=1
)

if exist "..\skillswap" (
    echo [FOUND] ..\skillswap
    set FOUND=1
)

REM Check common project locations
for /d %%d in (..\*) do (
    if exist "%%d\src\main\java" (
        echo [FOUND] %%d ^(Java project detected^)
        set FOUND=1
    )
)

echo.
if %FOUND%==0 (
    echo [INFO] No Java projects found in parent directory
    echo.
    echo Please provide the full path to your Java project
    echo Example: C:\projects\PaiementManagement
)

echo.
echo ============================================
echo.
echo To run analysis on a specific project:
echo.
echo python run_agent.py run --dry-run --repo-path "C:\path\to\project"
echo.
pause
