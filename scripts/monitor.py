#!/usr/bin/env python3
"""Simple monitoring script"""

import psutil
import time

def monitor():
    while True:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        
        print(f"\rCPU: {cpu:5.1f}% | RAM: {mem.percent:5.1f}% ({mem.used/1e9:.1f}/{mem.total/1e9:.1f}GB)", end="")
        time.sleep(2)

if __name__ == "__main__":
    try:
        print("Monitoring (Ctrl+C to stop)...")
        monitor()
    except KeyboardInterrupt:
        print("\nStopped")
