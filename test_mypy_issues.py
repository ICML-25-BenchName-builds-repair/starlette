"""
Test script to verify mypy issues.
"""
import sys
from typing import Dict, List, Optional, Union

def test_union_syntax():
    # Python 3.10+ syntax
    # var1: str | None = None  # This will fail on Python < 3.10
    
    # Compatible syntax
    var2: Optional[str] = None  # This works on all Python versions
    
    # Python 3.10+ syntax
    # var3: dict[str, str] | None = None  # This will fail on Python < 3.10
    
    # Compatible syntax
    var4: Optional[Dict[str, str]] = None  # This works on all Python versions
    
    # Python 3.10+ syntax
    # var5: list[str] = []  # This will fail on Python < 3.10
    
    # Compatible syntax
    var6: List[str] = []  # This works on all Python versions
    
    print("Union syntax test completed")

def test_tuple_unpacking():
    # Test the tuple unpacking issue in concurrency.py
    args = [(lambda: None, {"param": "value"})]
    
    for func, kwargs in args:
        print(f"Function: {func}, kwargs: {kwargs}")
    
    print("Tuple unpacking test completed")

if __name__ == "__main__":
    print(f"Python version: {sys.version}")
    test_union_syntax()
    test_tuple_unpacking()
    print("All tests passed")