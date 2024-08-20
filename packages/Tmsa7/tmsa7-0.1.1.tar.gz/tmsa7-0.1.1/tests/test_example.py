# tests/test_examples.py
import sys
import os

# Add the parent directory of the project to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Tmsa7.core.example import examples

# Now you can proceed with your tests
example = examples()
example.ai()
