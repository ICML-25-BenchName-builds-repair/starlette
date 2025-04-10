#!/usr/bin/env python3
"""
Test script to verify mypy issues in the codebase.
"""

import sys
import typing
from pathlib import Path

def test_concurrency_issue():
    """Test the unpacking issue in concurrency.py"""
    # The issue is in this line:
    # for func, kwargs in args:
    #     task_group.start_soon(run, functools.partial(func, **kwargs))
    
    # Simulate the issue with a simple example
    args = [(lambda: None, {}), (lambda: None,)]  # Second tuple has only one element
    
    try:
        for func, kwargs in args:
            print(f"Function: {func}, kwargs: {kwargs}")
        print("No error in concurrency test - this is unexpected!")
    except ValueError as e:
        print(f"Expected error in concurrency test: {e}")

def test_union_syntax():
    """Test the union syntax issue"""
    # Python 3.10+ syntax
    if sys.version_info >= (3, 10):
        # This will work in Python 3.10+
        def modern_union() -> str | None:
            return None
        print("Modern union syntax works in this Python version")
    else:
        # This will fail in Python < 3.10
        try:
            # This is a syntax error in Python < 3.10, so we can't actually run it
            # def modern_union() -> str | None:
            #     return None
            print("Would fail with syntax error in Python < 3.10")
        except SyntaxError as e:
            print(f"Expected syntax error: {e}")
    
    # This works in all Python versions
    def classic_union() -> typing.Optional[str]:
        return None
    print("Classic union syntax works in all Python versions")

def test_subscriptable_types():
    """Test the subscriptable types issue"""
    # Python 3.9+ syntax
    if sys.version_info >= (3, 9):
        # This will work in Python 3.9+
        def modern_dict() -> dict[str, str]:
            return {"key": "value"}
        def modern_list() -> list[str]:
            return ["item"]
        print("Modern subscriptable types work in this Python version")
    else:
        # This will fail in Python < 3.9
        try:
            # This is a type error in Python < 3.9
            # def modern_dict() -> dict[str, str]:
            #     return {"key": "value"}
            print("Would fail with type error in Python < 3.9")
        except TypeError as e:
            print(f"Expected type error: {e}")
    
    # This works in all Python versions
    def classic_dict() -> typing.Dict[str, str]:
        return {"key": "value"}
    def classic_list() -> typing.List[str]:
        return ["item"]
    print("Classic subscriptable types work in all Python versions")

if __name__ == "__main__":
    print(f"Python version: {sys.version}")
    print("\nTesting concurrency issue:")
    test_concurrency_issue()
    print("\nTesting union syntax:")
    test_union_syntax()
    print("\nTesting subscriptable types:")
    test_subscriptable_types()