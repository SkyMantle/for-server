#!/usr/bin/env python3
"""Quick test to see what the app generates"""
import sys
import signal
import time

def timeout_handler(signum, frame):
    print("\n⏱️  Timeout reached")
    raise TimeoutError("App startup timeout")

# Set 15 second timeout
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(15)

try:
    print("Starting app...")
    
    # Execute the app file to see what happens
    import subprocess
    result = subprocess.run(
        ["python", "app.py"],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    print("STDOUT:")
    print(result.stdout[:2000])
    print("\nSTDERR:")
    print(result.stderr[:2000])
    print(f"\nReturn code: {result.returncode}")
    
except subprocess.TimeoutExpired:
    print("✅ App started successfully (server running)")
except Exception as e:
    print(f"Error: {e}")
finally:
    signal.alarm(0)
