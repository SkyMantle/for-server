#!/usr/bin/env python3
"""Inspect the demo object structure"""
import sys
sys.path.insert(0, '.')

# Suppress notifications and launch
import os
os.environ['GRADIO_ANALYTICS_ENABLED'] = 'False'

# Import but don't launch
import importlib.util
spec = importlib.util.spec_from_file_location("app", "app.py")
app = importlib.util.module_from_spec(spec)

try:
    # Load module without executing __main__
    code = open('app.py').read()
    # Remove the __main__ block
    code_lines = code.split('\n')
    filtered_lines = []
    in_main = False
    for line in code_lines:
        if 'if __name__ == "__main__":' in line:
            in_main = True
        if not in_main:
            filtered_lines.append(line)
    
    filtered_code = '\n'.join(filtered_lines)
    
    # Execute to create the demo object
    namespace = {}
    exec(filtered_code, namespace)
    
    demo = namespace.get('demo')
    
    if demo:
        print("✅ Demo object created successfully")
        print(f"Demo type: {type(demo)}")
        print(f"Demo has config: {hasattr(demo, 'config')}")
        
        if hasattr(demo, 'blocks'):
            print(f"Number of blocks: {len(demo.blocks)}")
            
            # Count tabs
            tab_count = 0
            for i, block in enumerate(demo.blocks):
                block_type = type(block).__name__
                if 'Tab' in block_type:
                    tab_count += 1
                    print(f"  Block {i}: {block_type}")
            
            print(f"Total tab-related blocks: {tab_count}")
    else:
        print("❌ Could not create demo object")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
