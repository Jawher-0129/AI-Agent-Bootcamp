#!/bin/bash
# Sonar AI Agent - Linux/Mac Helper Script

set -e

echo "============================================"
echo "   Sonar AI Agent - Setup & Runner"
echo "============================================"
echo

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 not found! Please install Python 3.8+"
    exit 1
fi

echo "[OK] Python found: $(python3 --version)"
echo

# Check .env
if [ ! -f ".env" ]; then
    echo "[INFO] Creating .env from template..."
    cp .env.example .env
    echo "[ACTION REQUIRED] Please edit .env with your credentials"
    echo "Opening .env in default editor..."
    ${EDITOR:-nano} .env
    echo
fi

echo "============================================"
echo "   Choose an option:"
echo "============================================"
echo "1. Install dependencies"
echo "2. Run dry-run (test mode)"
echo "3. Run production (apply patches)"
echo "4. View last report"
echo "5. Exit"
echo

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo
        echo "Installing dependencies..."
        python3 -m pip install -r requirements.txt
        echo
        echo "[SUCCESS] Dependencies installed!"
        ;;
    2)
        echo
        echo "Running in DRY-RUN mode (no changes will be applied)..."
        echo
        python3 run_agent.py run --dry-run
        echo
        echo "[DONE] Check sonar_ai_report.md for results"
        ;;
    3)
        echo
        echo "============================================"
        echo "   WARNING: PRODUCTION MODE"
        echo "============================================"
        echo "This will apply patches to your code!"
        echo "Make sure you have:"
        echo "  1. Reviewed the dry-run results"
        echo "  2. Committed your current changes"
        echo "  3. Backed up your code"
        echo
        read -p "Are you sure? (yes/no): " confirm
        if [ "$confirm" != "yes" ]; then
            echo "Cancelled."
            exit 0
        fi
        echo
        echo "Running in PRODUCTION mode..."
        echo
        python3 run_agent.py run
        echo
        echo "[DONE] Check sonar_ai_report.md for results"
        ;;
    4)
        echo
        if [ -f "sonar_ai_report.md" ]; then
            echo "Opening report..."
            if command -v xdg-open &> /dev/null; then
                xdg-open sonar_ai_report.md
            elif command -v open &> /dev/null; then
                open sonar_ai_report.md
            else
                cat sonar_ai_report.md
            fi
        else
            echo "[ERROR] No report found. Run the agent first!"
        fi
        ;;
    5)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice!"
        exit 1
        ;;
esac

echo
echo "Goodbye!"
