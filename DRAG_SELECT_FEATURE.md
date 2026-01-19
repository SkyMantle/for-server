# 🖱️ Drag-to-Select Region Feature

## Overview
Users can now drag directly on the screenshot to select a custom screen region for streaming.

## How It Works

### 1. Click "🖱️ Select Screen Area" Button
- Captures full desktop screenshot
- Displays screenshot in the interface
- Injects drag selection JavaScript

### 2. Drag Selection
- **Hover over screenshot** - Cursor changes to crosshair
- **Click and drag** - Blue selection rectangle appears with coordinates
- **Release mouse** - Coordinates auto-populate in fields (X, Y, Width, Height)
- **Selection stays visible** for 3 seconds so you can verify

### 3. Start Recording
- Click "▶️ Start Recording Desktop"
- Only the selected region will be captured and analyzed

## Features

✅ **Web-based (no crashes)** - Uses browser canvas overlay, no system-level fullscreen issues
✅ **Real-time feedback** - Shows coordinates as you drag
✅ **Auto-populate fields** - No need to manually type coordinates
✅ **Smooth scaling** - Works correctly regardless of screenshot size or DPI
✅ **Visual handles** - Corner indicators show selection bounds
✅ **Persistent preview** - Selection stays visible for 3 seconds
✅ **Manual fallback** - Can still type coordinates if needed
✅ **Works on macOS** - No tkinter crashes, pure JavaScript solution

## Technical Details

**Files:**
- `app.py` - Main application with button handler
- `drag_selection.js` - JavaScript for drag detection and canvas overlay

**Technologies:**
- HTML5 Canvas API for drawing selection
- Event listeners for mouse tracking
- DOM mutation observer for detecting new screenshots
- Automatic field population with event dispatch

**Browser Compatibility:**
- Works in all modern browsers (Chrome, Firefox, Safari, Edge)
- Requires canvas support
- Uses standard DOM APIs

## Usage Flow

```
1. Click "🖱️ Select Screen Area" button
   ↓
2. Screenshot appears with instructions
   ↓
3. Drag on screenshot to select region
   ↓
4. Fields auto-fill (X, Y, Width, Height)
   ↓
5. Click "▶️ Start Recording Desktop"
   ↓
6. Only selected region streams to satellite comparison
```

## Fallback: Manual Entry

If drag selection doesn't work, you can manually enter:
- **X**: Horizontal position (pixels from left edge)
- **Y**: Vertical position (pixels from top edge)
- **Width**: Region width in pixels
- **Height**: Region height in pixels

Then click "🖱️ Clear Selection" to reset to full screen.

## Future Enhancements

- [ ] Save/load region presets
- [ ] Multiple region support
- [ ] Region history
- [ ] Keyboard shortcuts for precise adjustments
- [ ] Touch device support for tablets/mobile
