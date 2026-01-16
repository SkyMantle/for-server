#!/usr/bin/env python3
"""System requirements checker"""

import sys
import subprocess

def check_python():
    v = sys.version_info
    print(f"Python: {v.major}.{v.minor}.{v.micro}", end=" ")
    if v.major >= 3 and v.minor >= 8:
        print("✅")
        return True
    print("❌ (need 3.8+)")
    return False

def check_gpu():
    try:
        import torch
        print(f"PyTorch: {torch.__version__}", end=" ")
        if torch.cuda.is_available():
            print(f"✅ (GPU: {torch.cuda.get_device_name(0)})")
            return True
        print("⚠️  (CPU only)")
        return False
    except:
        print("❌ (not installed)")
        return False

def check_dependencies():
    packages = ['gradio', 'numpy', 'PIL', 'requests', 'plotly']
    all_ok = True
    for pkg in packages:
        try:
            if pkg == 'PIL':
                __import__('PIL')
            else:
                __import__(pkg)
            print(f"{pkg}: ✅")
        except:
            print(f"{pkg}: ❌")
            all_ok = False
    return all_ok

if __name__ == "__main__":
    print("System Check")
    print("=" * 40)
    check_python()
    check_gpu()
    print()
    check_dependencies()
