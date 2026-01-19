"""
Simple Flask web app for interactive screenshot and drag-to-select region
Runs on port 5000 as a separate web service
"""

from flask import Flask, render_template_string, request, send_file
from PIL import Image
import mss
import io
import base64

app = Flask(__name__)

# HTML template with embedded CSS and JavaScript
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🖱️ Screen Region Selector</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 90vw;
            max-height: 90vh;
            overflow-y: auto;
            padding: 30px;
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 24px;
        }
        
        .subtitle {
            color: #666;
            margin-bottom: 20px;
            font-size: 14px;
        }
        
        .controls {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        
        button {
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .btn-primary {
            background: #667eea;
            color: white;
        }
        
        .btn-primary:hover {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .btn-secondary {
            background: #e0e0e0;
            color: #333;
        }
        
        .btn-secondary:hover {
            background: #d0d0d0;
        }
        
        .screenshot-container {
            position: relative;
            display: inline-block;
            margin-bottom: 20px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
        }
        
        #screenshot {
            display: block;
            max-width: 100%;
            height: auto;
        }
        
        #canvas {
            position: absolute;
            top: 0;
            left: 0;
            cursor: crosshair;
            z-index: 100;
        }
        
        .info-box {
            background: #f5f5f5;
            border-left: 4px solid #667eea;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 20px;
            font-size: 13px;
            color: #555;
            line-height: 1.6;
        }
        
        .coordinates {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .coord-item {
            background: #f9f9f9;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            padding: 12px;
            text-align: center;
        }
        
        .coord-label {
            font-size: 11px;
            color: #999;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }
        
        .coord-value {
            font-size: 18px;
            font-weight: bold;
            color: #667eea;
            font-family: 'Monaco', 'Courier New', monospace;
        }
        
        .copy-button {
            padding: 8px 16px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            margin-top: 10px;
            width: 100%;
        }
        
        .copy-button:hover {
            background: #5568d3;
        }
        
        .copy-button.copied {
            background: #4caf50;
        }
        
        .status {
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 20px;
            font-size: 13px;
            display: none;
        }
        
        .status.show {
            display: block;
        }
        
        .status.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .status.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .instructions {
            background: #e3f2fd;
            border: 1px solid #bbdefb;
            border-radius: 6px;
            padding: 15px;
            margin-bottom: 20px;
            font-size: 13px;
            color: #1565c0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🖱️ Screen Region Selector</h1>
        <p class="subtitle">Drag to select a region from your screen</p>
        
        <div class="instructions">
            <strong>How to use:</strong>
            <ol style="margin-top: 8px; margin-left: 20px;">
                <li>Click "📸 Capture Screenshot" to grab your screen</li>
                <li>Drag on the image to select a region</li>
                <li>Coordinates will appear automatically</li>
                <li>Click "📋 Copy Coordinates" to copy to clipboard</li>
            </ol>
        </div>
        
        <div class="controls">
            <button class="btn-primary" onclick="captureScreenshot()">📸 Capture Screenshot</button>
            <button class="btn-secondary" onclick="resetSelection()">🔄 Reset</button>
        </div>
        
        <div id="status" class="status"></div>
        
        <div id="screenshotArea" style="display: none;">
            <div class="screenshot-container">
                <img id="screenshot" alt="Desktop Screenshot">
                <canvas id="canvas"></canvas>
            </div>
            
            <div class="coordinates">
                <div class="coord-item">
                    <div class="coord-label">X</div>
                    <div class="coord-value" id="coordX">0</div>
                </div>
                <div class="coord-item">
                    <div class="coord-label">Y</div>
                    <div class="coord-value" id="coordY">0</div>
                </div>
                <div class="coord-item">
                    <div class="coord-label">Width</div>
                    <div class="coord-value" id="coordW">640</div>
                </div>
                <div class="coord-item">
                    <div class="coord-label">Height</div>
                    <div class="coord-value" id="coordH">420</div>
                </div>
            </div>
            
            <button class="copy-button" onclick="copyCoordinates()">📋 Copy: X, Y, Width, Height</button>
        </div>
    </div>

    <script>
        let canvas, ctx, img;
        let isDrawing = false;
        let startX, startY;
        let lastX = 0, lastY = 0, lastW = 640, lastH = 420;
        
        function showStatus(message, type = 'success') {
            const status = document.getElementById('status');
            status.textContent = message;
            status.className = 'status show ' + type;
            setTimeout(() => {
                status.classList.remove('show');
            }, 3000);
        }
        
        function captureScreenshot() {
            fetch('/screenshot')
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        showStatus('Error: ' + data.error, 'error');
                        return;
                    }
                    
                    img = document.getElementById('screenshot');
                    canvas = document.getElementById('canvas');
                    ctx = canvas.getContext('2d');
                    
                    img.src = 'data:image/png;base64,' + data.screenshot;
                    
                    img.onload = () => {
                        canvas.width = img.naturalWidth;
                        canvas.height = img.naturalHeight;
                        canvas.style.width = img.offsetWidth + 'px';
                        canvas.style.height = img.offsetHeight + 'px';
                        
                        document.getElementById('screenshotArea').style.display = 'block';
                        drawPreselectedArea();
                        attachCanvasEvents();
                        showStatus('Screenshot captured! Drag to select region.');
                    };
                })
                .catch(error => {
                    showStatus('Error capturing screenshot: ' + error, 'error');
                });
        }
        
        function drawPreselectedArea() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            drawSelection(lastX, lastY, lastX + lastW, lastY + lastH);
        }
        
        function drawSelection(fromX, fromY, toX, toY) {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            const x = Math.min(fromX, toX);
            const y = Math.min(fromY, toY);
            const w = Math.abs(toX - fromX);
            const h = Math.abs(toY - fromY);
            
            // Semi-transparent blue fill
            ctx.fillStyle = 'rgba(102, 126, 234, 0.15)';
            ctx.fillRect(x, y, w, h);
            
            // Blue border
            ctx.strokeStyle = '#667eea';
            ctx.lineWidth = 3;
            ctx.strokeRect(x, y, w, h);
            
            // Corner handles
            const handleSize = 12;
            ctx.fillStyle = '#667eea';
            const handles = [
                {x: x, y: y},
                {x: x + w, y: y},
                {x: x, y: y + h},
                {x: x + w, y: y + h}
            ];
            handles.forEach(h => {
                ctx.fillRect(h.x - handleSize/2, h.y - handleSize/2, handleSize, handleSize);
            });
            
            // Display coordinates
            const text = `X: ${Math.round(x)}  Y: ${Math.round(y)}  W: ${Math.round(w)}  H: ${Math.round(h)}`;
            ctx.fillStyle = '#667eea';
            ctx.font = 'bold 16px monospace';
            ctx.fillText(text, x + 15, y + 35);
            
            // Update displayed values
            document.getElementById('coordX').textContent = Math.round(x);
            document.getElementById('coordY').textContent = Math.round(y);
            document.getElementById('coordW').textContent = Math.round(w);
            document.getElementById('coordH').textContent = Math.round(h);
            
            lastX = Math.round(x);
            lastY = Math.round(y);
            lastW = Math.round(w);
            lastH = Math.round(h);
        }
        
        function getCanvasCoordinates(e) {
            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            return {
                x: (e.clientX - rect.left) * scaleX,
                y: (e.clientY - rect.top) * scaleY
            };
        }
        
        function attachCanvasEvents() {
            canvas.addEventListener('mousedown', (e) => {
                isDrawing = true;
                const coords = getCanvasCoordinates(e);
                startX = coords.x;
                startY = coords.y;
            });
            
            canvas.addEventListener('mousemove', (e) => {
                if (!isDrawing) return;
                const coords = getCanvasCoordinates(e);
                drawSelection(startX, startY, coords.x, coords.y);
            });
            
            canvas.addEventListener('mouseup', (e) => {
                isDrawing = false;
            });
        }
        
        function resetSelection() {
            lastX = 0;
            lastY = 0;
            lastW = 640;
            lastH = 420;
            if (canvas && img) {
                drawPreselectedArea();
                showStatus('Selection reset to default 640×420');
            }
        }
        
        function copyCoordinates() {
            const text = `${lastX},${lastY},${lastW},${lastH}`;
            navigator.clipboard.writeText(text).then(() => {
                const btn = event.target;
                const original = btn.textContent;
                btn.textContent = '✅ Copied!';
                btn.classList.add('copied');
                setTimeout(() => {
                    btn.textContent = original;
                    btn.classList.remove('copied');
                }, 2000);
            });
        }
        
        // Capture screenshot on load
        window.addEventListener('load', captureScreenshot);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/screenshot', methods=['GET'])
def get_screenshot():
    try:
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
            
            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            return {
                'screenshot': b64,
                'width': screenshot.size[0],
                'height': screenshot.size[1]
            }
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    print("🖱️  Screenshot Selector Tool")
    print("━" * 50)
    print("🌐 Open: http://localhost:5001")
    print("━" * 50)
    print("\nFeatures:")
    print("  • Drag to select screen regions")
    print("  • Preselected 640×420 area")
    print("  • Copy coordinates to clipboard")
    print("  • Real-time coordinate display")
    print("\nPress Ctrl+C to stop")
    print()
    app.run(host='0.0.0.0', port=5001, debug=False)
