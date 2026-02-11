"""
Sonar AI Agent - Entry point script
This wrapper allows running the agent without package installation
"""

import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Now we can import and run
from sonar_ai_agent.main import main

if __name__ == "__main__":
    main()
