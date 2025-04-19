import sys
import os
import urllib3

urllib3.disable_warnings()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from app import app

if __name__ == "__main__":
    print("Starting RubberDucky...")
    app()
