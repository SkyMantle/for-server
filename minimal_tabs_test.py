#!/usr/bin/env python3
"""Minimal test to verify tab structure works"""
import gradio as gr

print("Creating demo with tabs...")

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Test App")
    
    print("  - Creating Tabs container...")
    with gr.Tabs():
        print("    - Creating Tab 1...")
        with gr.TabItem("🖼️ Tab One"):
            gr.Markdown("## Tab 1 Content")
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### Left Side")
                    btn1 = gr.Button("Button 1")
                with gr.Column(scale=2):
                    gr.Markdown("### Right Side")
                    txt1 = gr.Textbox(label="Text 1")
            
            btn1.click(lambda: "Clicked!", outputs=[txt1])
        
        print("    - Creating Tab 2...")
        with gr.TabItem("🎥 Tab Two"):
            gr.Markdown("## Tab 2 Content")
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### Config")
                    inp = gr.Radio(choices=["A", "B"], value="A")
                with gr.Column(scale=2):
                    gr.Markdown("### Display")
                    img = gr.Image(label="Image")
            
            inp.change(lambda x: gr.update(visible=x=="A"), inputs=[inp], outputs=[img])
    
    print("  - Tabs created successfully!")
    
    gr.Markdown("### End of content")

print("\nLaunching demo...")
if __name__ == "__main__":
    demo.launch(server_port=7862, share=False, show_error=True)
