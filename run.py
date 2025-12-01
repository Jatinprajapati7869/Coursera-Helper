import sys
import os

# Add the current directory to sys.path to ensure 'coursera' package is found
# This allows running the script from the root directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from coursera.gui.maingui import main

if __name__ == "__main__":
    main()
