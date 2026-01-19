#!/usr/bin/env python3
"""Test script to verify tabs render correctly"""
import gradio as gr

with gr.Blocks() as demo:
    gr.Markdown("# Test Tabs")
    
    with gr.Tabs():
        with gr.TabItem("📸 Tab 1"):
            gr.Markdown("### Tab 1 Content")
            gr.Textbox(label="Input 1")
        
        with gr.TabItem("🎥 Tab 2"):
            gr.Markdown("### Tab 2 Content")
            gr.Textbox(label="Input 2")
            gr.Button("Click Me")

if __name__ == "__main__":
    demo.launch(server_port=7862, share=False)
