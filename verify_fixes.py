#!/usr/bin/env python3
"""
Script to verify that the specific errors mentioned in the issue description have been fixed.
"""

import subprocess
import sys
from pathlib import Path

def check_specific_errors():
    """Check that the specific errors mentioned in the issue are fixed."""
    print("=== Verifying Fixes for Issue Description Errors ===")
    
    # The specific files and lines mentioned in the issue
    test_cases = [
        {
            "file": "starlette/concurrency.py",
            "expected_error": "Need more than 1 value to unpack (2 expected)",
            "line": 32
        },
        {
            "file": "starlette/_utils.py", 
            "expected_error": "X | Y syntax for unions requires Python 3.10",
            "line": 77
        },
        {
            "file": "starlette/exceptions.py",
            "expected_error": "X | Y syntax for unions requires Python 3.10",
            "line": 12
        },
        {
            "file": "starlette/exceptions.py",
            "expected_error": "X | Y syntax for unions requires Python 3.10", 
            "line": 13
        },
        {
            "file": "starlette/exceptions.py",
            "expected_error": '"dict" is not subscriptable, use "typing.Dict" instead',
            "line": 13
        },
        {
            "file": "starlette/exceptions.py",
            "expected_error": "X | Y syntax for unions requires Python 3.10",
            "line": 30
        },
        {
            "file": "starlette/exceptions.py",
            "expected_error": '"list" is not subscriptable, use "typing.List" instead',
            "line": 59
        }
    ]
    
    repo_dir = Path(__file__).parent
    all_fixed = True
    
    for case in test_cases:
        print(f"\n--- Checking {case['file']}:{case['line']} ---")
        try:
            result = subprocess.run(
                ["venv/bin/mypy", case["file"]],
                cwd=repo_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Check if the specific error is present
            error_found = case["expected_error"] in result.stdout
            line_mentioned = f":{case['line']}:" in result.stdout
            
            if error_found and line_mentioned:
                print(f"❌ ERROR STILL PRESENT: {case['expected_error']}")
                all_fixed = False
            else:
                print(f"✅ FIXED: No longer shows '{case['expected_error']}'")
                
        except Exception as e:
            print(f"Error checking {case['file']}: {e}")
            all_fixed = False
    
    return all_fixed

def check_files_individually():
    """Check each file mentioned in the issue individually."""
    print("\n=== Individual File Checks ===")
    
    files = ["starlette/concurrency.py", "starlette/_utils.py", "starlette/exceptions.py"]
    repo_dir = Path(__file__).parent
    all_passed = True
    
    for file_path in files:
        print(f"\n--- Checking {file_path} ---")
        try:
            result = subprocess.run(
                ["venv/bin/mypy", file_path],
                cwd=repo_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print(f"✅ {file_path}: PASSED")
            else:
                print(f"❌ {file_path}: FAILED")
                print(result.stdout)
                all_passed = False
                
        except Exception as e:
            print(f"Error checking {file_path}: {e}")
            all_passed = False
    
    return all_passed

def main():
    print("=== Verification Script for Issue Description Fixes ===")
    
    # Check if we're in the right directory
    repo_dir = Path(__file__).parent
    if not (repo_dir / "starlette").exists():
        print("Error: starlette directory not found.")
        sys.exit(1)
    
    if not (repo_dir / "venv" / "bin" / "mypy").exists():
        print("Error: mypy not found in venv.")
        sys.exit(1)
    
    # Run checks
    errors_fixed = check_specific_errors()
    files_passed = check_files_individually()
    
    print("\n=== SUMMARY ===")
    if errors_fixed:
        print("✅ All specific errors mentioned in the issue description have been fixed!")
    else:
        print("❌ Some specific errors from the issue description are still present.")
        
    if files_passed:
        print("✅ All files mentioned in the issue description pass mypy checks!")
    else:
        print("❌ Some files mentioned in the issue description still have mypy errors.")
    
    if errors_fixed and files_passed:
        print("\n🎉 SUCCESS: All issues mentioned in the issue description have been resolved!")
        return 0
    else:
        print("\n💥 FAILURE: Some issues from the issue description remain unfixed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())