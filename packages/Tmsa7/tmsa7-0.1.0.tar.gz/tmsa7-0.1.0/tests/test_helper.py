# tests/test_helper.py
import sys
import os

# Add the parent directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Tmsa7.core.helper import help

# Now you can proceed with your tests
helper = help()
helper.python()
help.nlp