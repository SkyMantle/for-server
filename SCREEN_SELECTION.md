# Screen Area Selection - Drag & Select Feature

## Overview
Added interactive **drag-to-select** screen area capture functionality! Now you can easily select exactly which part of your screen to capture and stream.

## What's New

### 🎯 "Select Screen Area" Button
- Opens a full-screen overlay with crosshair cursor
- Dim entire screen for better visibility
- Drag to draw selection rectangle
- Shows live coordinates and dimensions while dragging
- Minimum selection size: 50x50 pixels

### Features
- ✅ Real-time coordinate display during dragging
- ✅ Visual selection rectangle with lime green border
- ✅ Instructions overlay on screen
- ✅ Press ESC to cancel
- ✅ Auto-populate region fields with selected coordinates
- ✅ Clear selection button to revert to full screen
- ✅ Region status indicator in UI

## How to Use

### Step 1: Open the App
```bash
source .venv/bin/activate
python start_app.sh
```

### Step 2: Go to "🎥 Real-Time Streaming" Tab

### Step 3: Click "🖱️ Select Screen Area" Button
- Full screen will dim
- Crosshair cursor appears
- Instructions displayed at top

### Step 4: Drag to Select Region
- Click and drag to draw rectangle
- Live coordinates shown above selection
- Must be at least 50×50 pixels
- Release to confirm

### Step 5: Configure & Stream
- Region X, Y, Width, Height auto-populate
- Configure coordinates and algorithm settings
- Click "▶️ Start Recording Desktop"
- Only your selected area will be captured!

### Step 6: Stop & Clear (Optional)
- Click "⏹️ Stop Recording" to stop
- Click "🗑️ Clear Selection" to reset to full screen

## Examples

### Capture Center 800x600
1. Click "🖱️ Select Screen Area"
2. Drag from (560, 240) to (1360, 840)
3. Result: X=560, Y=240, W=800, H=600

### Capture Top-Left Corner
1. Click "🖱️ Select Screen Area"
2. Drag from (0, 0) to (640, 480)
3. Result: X=0, Y=0, W=640, H=480

### Capture Right Half of Screen
1. Click "🖱️ Select Screen Area"
2. Drag from (960, 0) to (1920, 1080)
3. Result: X=960, Y=0, W=960, H=1080

## Technical Details

### ScreenSelector Class
Located in `app.py`, implements:
- `on_press()` - Starts selection on mouse click
- `on_drag()` - Draws selection rectangle while dragging
- `on_release()` - Confirms selection and closes overlay
- `on_cancel()` - Cancels selection on ESC press

### Key Technologies
- **tkinter** - Native GUI overlay
- **Canvas** - Real-time drawing
- **Full-screen mode** - Overlay covers entire display
- **Semi-transparent** - 30% opacity (alpha=0.3)

### Selection Validation
- Minimum size: 50×50 pixels
- Invalid selections show error message
- User must try again

### Region Storage
```python
selected_region = (x, y, width, height)
# Passed to start_desktop_capture()
# Used to set desktop_region for mss.mss() capture
```

## Features & Benefits

| Feature | Benefit |
|---------|---------|
| Drag to select | Easy visual selection |
| Full-screen overlay | See exactly what you're capturing |
| Live coordinates | Know exact pixel positions |
| Crosshair cursor | Precise positioning |
| ESC to cancel | Easy exit without selecting |
| Auto-populate fields | No manual coordinate entry |
| Status indicator | Visual feedback |
| Clear button | Quick reset to full screen |

## Files Modified

### app.py
1. **Imports added:**
   - `import tkinter as tk`
   - `from tkinter import Canvas`
   - `import platform`
   - `import mss` (with fallback)

2. **New global variable:**
   - `selected_region = None` - Stores (x, y, width, height)

3. **New function:**
   - `select_screen_area()` - Opens selection overlay, returns coordinates

4. **New class:**
   - `ScreenSelector` - Handles UI and user interaction

5. **Updated function:**
   - `start_desktop_capture()` - Uses `selected_region` if available

6. **New UI elements in streaming tab:**
   - "🖱️ Select Screen Area" button
   - Region status display
   - Region coordinate fields (X, Y, Width, Height)
   - "🗑️ Clear Selection" button

7. **New event handlers:**
   - `select_screen_area_handler()` - Button click handler
   - `clear_region_handler()` - Clear button handler

## Performance Impact

- **Selection time:** <1 second to open/close overlay
- **Streaming performance:** Same FPS with smaller regions
- **CPU usage:** Smaller regions = less CPU/GPU load
- **Memory:** Minimal (only stores coordinates)

## Troubleshooting

### Screen Overlay Doesn't Appear
- Ensure tkinter is installed: `pip install tk` (usually included)
- Check system permissions for screen capture
- Try clicking button again

### Selection Too Slow
- Might be waiting for tkinter window to appear
- Ensure no other full-screen apps are open
- Press ESC to cancel and try again

### Coordinates Not Appearing in Fields
- Ensure selection is >= 50×50 pixels
- Try selecting a larger area
- Check browser console for errors

### Wrong Region Selected
- Click "🗑️ Clear Selection" to reset
- Click "🖱️ Select Screen Area" again
- Be more precise with your drag

## Advanced Tips

### Multi-Monitor Setup
- Select region only captures the area you drag
- Coordinates are relative to entire virtual desktop
- If spanning monitors, it works correctly

### Custom Python Script
You can also select regions programmatically:
```python
from app import select_screen_area
region = select_screen_area()
if region:
    x, y, w, h = region
    print(f"Selected: X={x}, Y={y}, W={w}, H={h}")
```

### Combine with Other Tools
- Use with screen recording software
- Compare specific app windows
- Focus on particular drone camera view

## Future Enhancements

Possible improvements:
- [ ] Save region presets
- [ ] Keyboard shortcuts (S for select)
- [ ] Mouse wheel zoom on overlay
- [ ] Grid/guides overlay
- [ ] Common presets (full screen, half, quarters)
- [ ] Region history

## Summary

The new drag-to-select feature makes it **super easy** to capture exactly the part of your screen you want! 

**Quick workflow:**
1. Click "🖱️ Select Screen Area"
2. Drag to select
3. Click "▶️ Start Recording"
4. Done! 🚀

Enjoy precise screen region capture! 📺✨
