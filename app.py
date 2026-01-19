from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image
from io import BytesIO
import base64
import threading
import time
import os
import platform

# Your required libraries (keep all original imports)
import torch
import torchvision.transforms as T
from torchvision.models import resnet50, ResNet50_Weights
import numpy as np
import requests
from functools import lru_cache
import hashlib
try:
    import pyautogui
except ImportError:
    pyautogui = None
try:
    import cv2
except ImportError:
    cv2 = None
try:
    import mss
except ImportError:
    mss = None

app = Flask(__name__, template_folder='templates')

# GPU setup
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# Model lazy loading (keep your original code here - I've left placeholders)
_model = None
_model_loaded = False
def get_model():
    global _model, _model_loaded
    if not _model_loaded:
        print("Loading ResNet50...")
        _model = resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)
        _model = torch.nn.Sequential(*list(_model.children())[:-1])
        _model = _model.to(device)
        _model.eval()
        if device.type == 'cuda':
            torch.backends.cudnn.benchmark = True
        _model_loaded = True
    return _model

preprocess = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# ... PASTE ALL YOUR OTHER FUNCTIONS HERE (download_satellite_tile, embeddings, compare_images, etc.) ...

# ================== SMART DESKTOP CAPTURE ==================

# Detect environment: local GUI vs headless server
IS_HEADLESS = (
    os.environ.get('DISPLAY') is None or           # No X server (Linux headless)
    'RAILWAY' in os.environ or                     # Railway env var
    'RENDER' in os.environ or                      # Render env var
    platform.system() == 'Linux' and not os.getenv('XDG_SESSION_TYPE')  # Extra Linux headless check
)

print(f"[INFO] Running in {'HEADLESS' if IS_HEADLESS else 'GUI'} mode (pyautogui: {'available' if pyautogui else 'not available'})")

def capture_desktop_screenshot(region=None):
    """
    Smart capture:
    - Local GUI: prefer pyautogui (better cursor, multi-monitor support)
    - Headless server: force mss (works without DISPLAY)
    """
    try:
        # Prefer pyautogui on local machines with GUI
        if not IS_HEADLESS and pyautogui:
            print("[DEBUG] Using pyautogui for capture (local GUI)")
            if region:
                return pyautogui.screenshot(region=region)
            return pyautogui.screenshot()

        # Headless or pyautogui not available → use mss
        if not mss:
            raise RuntimeError("mss library not installed - cannot capture screenshot on headless server")

        print("[DEBUG] Using mss for capture (headless/server mode)")
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # primary monitor
            if region:
                x, y, w, h = region
                mon = {"top": y, "left": x, "width": w, "height": h}
            else:
                mon = monitor
            screenshot = sct.grab(mon)
            return Image.frombytes("RGB", screenshot.size, screenshot.rgb)

    except Exception as e:
        print(f"[ERROR] Screenshot capture failed: {e}")
        return None

# ================== ROUTES ==================

@app.route('/get_screenshot')
def get_screenshot():
    img = capture_desktop_screenshot()
    if img:
        buf = BytesIO()
        img.save(buf, format="PNG", optimize=True, quality=75)
        b64 = base64.b64encode(buf.getvalue()).decode('ascii')
        return jsonify({'b64': b64})
    return jsonify({'error': 'Failed to capture screenshot'})

def start_desktop_capture(data):
    global desktop_stream_active, desktop_stream_thread, desktop_region
    
    if desktop_stream_active:
        return {"status": "⚠️ Already capturing"}
    
    x = int(data.get('x', 0))
    y = int(data.get('y', 0))
    w = int(data.get('w', 1920))
    h = int(data.get('h', 1080))
    
    if w < 64 or h < 64:
        return {"status": "❌ Region too small (min 64×64)"}
    
    desktop_region = (x, y, w, h) if (x > 0 or y > 0 or w < 1920 or h < 1080) else None
    desktop_stream_active = True
    
    def capture_loop():
        global desktop_last_frame, desktop_stats
        start_time = time.time()
        frame_count = 0
        while desktop_stream_active:
            img = capture_desktop_screenshot(desktop_region)
            if img:
                with desktop_stream_lock:
                    desktop_last_frame = img.copy()
                frame_count += 1
                if time.time() - start_time >= 1.0:
                    desktop_stats["fps"] = frame_count / (time.time() - start_time)
                    desktop_stats["frames"] += frame_count
                    start_time = time.time()
                    frame_count = 0
            time.sleep(0.04)
    
    desktop_stream_thread = threading.Thread(target=capture_loop, daemon=True)
    desktop_stream_thread.start()
    return {"status": "✅ Capture started"}

def stop_desktop_capture():
    global desktop_stream_active
    if not desktop_stream_active:
        return {"status": "Already stopped"}
    desktop_stream_active = False
    if desktop_stream_thread:
        desktop_stream_thread.join(timeout=2.0)
    return {"status": "⏹️ Capture stopped"}

@app.route('/get_frame')
def get_frame():
    with desktop_stream_lock:
        if desktop_last_frame:
            buf = BytesIO()
            desktop_last_frame.save(buf, format="PNG")
            buf.seek(0)
            return send_file(buf, mimetype='image/png')
    return '', 204

@app.route('/get_stats')
def get_stats():
    region_text = f"Custom {desktop_region}" if desktop_region else "Full screen"
    status = "🟢 Running" if desktop_stream_active else "🔴 Stopped"
    return jsonify({
        "status_text": f"### 📊 Live Stats\n- **Status**: {status}\n- **FPS**: {desktop_stats['fps']:.1f}\n- **Frames**: {desktop_stats['frames']}\n- **Region**: {region_text}"
    })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select_region')
def select_region():
    return render_template('select_region.html')

@app.route('/start_capture', methods=['POST'])
def start_capture():
    return jsonify(start_desktop_capture(request.json))

@app.route('/stop_capture', methods=['POST'])
def stop_capture():
    return jsonify(stop_desktop_capture())

if __name__ == '__main__':
    # Use Railway/Render provided port (important!)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)