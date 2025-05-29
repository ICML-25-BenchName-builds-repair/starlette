#!/usr/bin/env python3
"""
Script to reproduce and verify the mypy issues mentioned in the CI failure.
"""

import subprocess
import sys
from pathlib import Path

def run_mypy_check():
    """Run mypy check and return the result."""
    print("Running mypy check...")
    
    # Change to the repository directory
    repo_dir = Path(__file__).parent
    
    try:
        result = subprocess.run(
            ["venv/bin/mypy", "starlette"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        print(f"Exit code: {result.returncode}")
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
            
        return result.returncode == 0, result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        print("Mypy check timed out!")
        return False, "", "Timeout"
    except Exception as e:
        print(f"Error running mypy: {e}")
        return False, "", str(e)

def check_specific_files():
    """Check the specific files mentioned in the issue."""
    files_to_check = [
        "starlette/concurrency.py",
        "starlette/_utils.py", 
        "starlette/exceptions.py"
    ]
    
    repo_dir = Path(__file__).parent
    
    for file_path in files_to_check:
        print(f"\n--- Checking {file_path} ---")
        try:
            result = subprocess.run(
                ["venv/bin/mypy", file_path],
                cwd=repo_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            print(f"Exit code: {result.returncode}")
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
                
        except Exception as e:
            print(f"Error checking {file_path}: {e}")

def main():
    print("=== MyPy Issues Reproduction Script ===")
    print("This script reproduces the mypy issues from the CI failure.")
    
    # First check if we're in the right directory
    repo_dir = Path(__file__).parent
    if not (repo_dir / "starlette").exists():
        print("Error: starlette directory not found. Make sure you're in the repository root.")
        sys.exit(1)
    
    if not (repo_dir / "venv" / "bin" / "mypy").exists():
        print("Error: mypy not found in venv. Make sure dependencies are installed.")
        sys.exit(1)
    
    print("\n1. Running full mypy check...")
    success, stdout, stderr = run_mypy_check()
    
    print("\n2. Checking specific files...")
    check_specific_files()
    
    if success:
        print("\n✅ All mypy checks passed!")
        return 0
    else:
        print("\n❌ MyPy checks failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())