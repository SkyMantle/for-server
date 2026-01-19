#!/usr/bin/env python3
"""Debug script to check app UI structure"""
import sys
import json

# Read the app.py file
with open('app.py', 'r') as f:
    content = f.read()

# Check basic structure
print("=" * 60)
print("APP STRUCTURE CHECK")
print("=" * 60)

# Count important elements
counts = {
    'gr.Blocks': content.count('with gr.Blocks'),
    'gr.Tabs': content.count('with gr.Tabs()'),
    'gr.TabItem': content.count('with gr.TabItem('),
    'gr.Row': content.count('with gr.Row()'),
    'gr.Column': content.count('with gr.Column('),
}

for key, count in counts.items():
    print(f"{key}: {count}")

print("\n" + "=" * 60)
print("TAB ITEMS FOUND")
print("=" * 60)

# Find all TabItems
import re
tab_items = re.findall(r'with gr\.TabItem\("([^"]+)"\)', content)
for i, tab in enumerate(tab_items, 1):
    print(f"  {i}. {tab}")

print("\n" + "=" * 60)
print("CHECKING DEMO OBJECT")
print("=" * 60)

# Check if demo is created
if 'with gr.Blocks(theme=gr.themes.Soft()) as demo:' in content:
    print("✅ Demo object is created properly")
else:
    print("❌ Demo object creation not found")

# Check if demo.launch is called
if 'demo.launch' in content:
    print("✅ demo.launch() is called")
else:
    print("❌ demo.launch() is not called")

print("\n" + "=" * 60)
print("IMPORTS CHECK")
print("=" * 60)

# Check imports
imports_needed = ['gradio as gr', 'torch', 'cv2', 'threading']
for imp in imports_needed:
    if imp in content[:2000]:  # Check in first part of file (imports section)
        print(f"✅ {imp} imported")
    else:
        print(f"⚠️  {imp} may not be imported")

print("\n" + "=" * 60)
print("All checks complete!")
print("=" * 60)
