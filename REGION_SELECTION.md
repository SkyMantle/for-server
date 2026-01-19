# Desktop Region Selection Feature

## What's New

Added **region selection capability** to the desktop screen capture feature! Now you can choose to capture:
- **Full Screen** - Entire desktop (default)
- **Custom Region** - Specific area using X, Y, width, height coordinates

## Changes Made

### 1. Updated `start_desktop_capture()` Function
- Added 4 new parameters: `region_mode`, `region_x`, `region_y`, `region_w`, `region_h`
- Added global `desktop_region` variable to store selected region
- Modified capture logic to use `pyautogui.screenshot(region=(...))` for partial captures
- Falls back to full screen if region_mode is "Full Screen"

### 2. New Desktop Streaming Tab UI

**Screen Region Selection Panel:**
- **Capture Mode** - Radio button: "Full Screen" or "Custom Region"
- **Region X** - Top-left X coordinate (pixels) - shown only when Custom Region selected
- **Region Y** - Top-left Y coordinate (pixels) - shown only when Custom Region selected
- **Region Width** - Width in pixels (min 100) - shown only when Custom Region selected
- **Region Height** - Height in pixels (min 100) - shown only when Custom Region selected

**Dynamic Visibility:**
- Region input fields hide/show automatically based on selected capture mode
- Uses Gradio's `visible=False` parameter and `.change()` callback

### 3. Updated Button Handlers
- `start_desktop_handler()` now receives region parameters
- Passes all 10 parameters to `start_desktop_capture()`:
  - coords, radius, grid_size (search settings)
  - algo, comp (algorithm settings)
  - mode, x, y, w, h (region settings)

## How to Use

### Full Screen Capture (Default):
1. Select "Full Screen" mode
2. Set your search coordinates and algorithm preferences
3. Click "▶️ Start Recording Desktop"
4. Your entire screen will be captured and analyzed

### Custom Region Capture:
1. Select "Custom Region" mode
2. Region input fields will appear
3. Set coordinates:
   - **X**: Horizontal pixels from left edge (0 = left edge)
   - **Y**: Vertical pixels from top edge (0 = top edge)
   - **Width**: Width of region to capture
   - **Height**: Height of region to capture
4. Click "▶️ Start Recording Desktop"
5. Only the selected region will be captured

### Coordinate Examples:

#### Capture center of screen (assuming 1920x1080):
```
X: 640     (starts at 1/3 from left)
Y: 360     (starts at 1/3 from top)
Width: 640
Height: 480
```

#### Capture top-left corner:
```
X: 0
Y: 0
Width: 640
Height: 480
```

#### Capture specific window/area:
```
X: 100
Y: 200
Width: 800
Height: 600
```

## Technical Implementation

### Region Parameter Flow:
```
UI Input (region_mode, region_x, y, w, h)
    ↓
start_desktop_handler() [callback]
    ↓
start_desktop_capture(..., region_mode, x, y, w, h) [backend]
    ↓
Sets desktop_region = (x, y, w, h) or None
    ↓
capture_loop() uses pyautogui.screenshot(region=desktop_region)
    ↓
Captured frame displayed in real-time
```

### Code Changes:

**Desktop Streaming Globals:**
```python
desktop_region = None  # (x, y, width, height) or None for full screen
```

**Capture Logic:**
```python
if desktop_region is None:
    screenshot = pyautogui.screenshot()  # Full screen
else:
    x, y, w, h = desktop_region
    screenshot = pyautogui.screenshot(region=(x, y, w, h))  # Partial
```

**UI Toggle Function:**
```python
def toggle_region_inputs(mode):
    visible = mode == "Custom Region"
    return [
        gr.update(visible=visible),  # region_x
        gr.update(visible=visible),  # region_y
        gr.update(visible=visible),  # region_w
        gr.update(visible=visible)   # region_h
    ]

region_mode.change(
    fn=toggle_region_inputs,
    inputs=[region_mode],
    outputs=[region_x, region_y, region_w, region_h]
)
```

## Performance Notes

- **Full Screen**: Captures entire desktop, then resized to 640x480
- **Custom Region**: Captures only specified region, smaller regions = faster processing
- **Frame Rate**: ~30 FPS for both modes
- **CPU Usage**: Selecting smaller regions reduces CPU load

## Use Cases

1. **Focus on specific monitor** - Capture one monitor in multi-monitor setup
2. **Reduce CPU load** - Smaller regions process faster
3. **Privacy** - Capture only relevant part of screen
4. **Testing specific areas** - Compare specific windows or applications
5. **Multi-camera simulation** - Capture different regions as separate streams

## Files Modified

- `app.py`:
  - Added `desktop_region` global variable
  - Updated `start_desktop_capture()` function signature
  - Added region selection UI to streaming tab
  - Updated button handlers to pass region parameters
  - Fixed capture logic to support partial screenshots

## Running the App

```bash
source .venv/bin/activate
python app.py
```

Navigate to "🎥 Real-Time Streaming" tab and try both Full Screen and Custom Region modes!
