"""
Test script to verify mypy issues.
"""
import sys
from starlette import concurrency, _utils, exceptions

def test_concurrency():
    """Test the concurrency module."""
    print(f"Testing concurrency.py with Python {sys.version}")
    
def test_utils():
    """Test the _utils module."""
    print(f"Testing _utils.py with Python {sys.version}")
    
def test_exceptions():
    """Test the exceptions module."""
    print(f"Testing exceptions.py with Python {sys.version}")
    
if __name__ == "__main__":
    test_concurrency()
    test_utils()
    test_exceptions()
    print("All modules imported successfully")