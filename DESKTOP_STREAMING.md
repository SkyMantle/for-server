# Desktop Screen Capture & Streaming Setup

## Overview
The app now includes a **Desktop Screen Capture** tab that lets you record your desktop and compare it against satellite imagery in real-time.

## What Was Added

### 1. **pyautogui Library**
- Installed version 0.9.53
- Captures desktop screenshots at ~30 FPS
- Added to requirements.txt

### 2. **Desktop Capture Module** (in app.py)
New functions added:

- **`start_desktop_capture()`** - Starts capturing desktop in background thread
  - Captures screenshots continuously
  - Processes every 3rd frame (reduces CPU load)
  - Compares frames against satellite tiles
  - Stores latest frame for display

- **`stop_desktop_capture()`** - Stops the capture thread gracefully

- **`get_desktop_frame_display()`** - Returns current desktop screenshot

- **`get_desktop_stats_display()`** - Returns stats (FPS, frame count, similarity score)

### 3. **Global Variables**
- `desktop_stream_active` - Thread control flag
- `desktop_stream_thread` - Background capture thread
- `desktop_last_frame` - Latest captured frame
- `desktop_stats` - Recording statistics
- `desktop_stream_lock` - Thread synchronization

### 4. **New UI Tab: "🖥️ Desktop Screen Capture & Analysis"**

#### Controls:
- **Search Coordinates** - Target location (lat, lon)
- **Search Radius** - Area to cover (km)
- **Grid Size** - Satellite tile coverage
- **Algorithm** - Choice of embedding methods
- **Comparison Method** - Similarity scoring algorithm
- **Start/Stop Buttons** - Control recording
- **Refresh Buttons** - Manual frame/stats update

#### Display:
- **Live Desktop Feed** - Shows captured screen in real-time
- **Analysis & Statistics** - FPS, frame count, similarity scores

## How to Use

### 1. **Activate Virtual Environment**
```bash
source .venv/bin/activate
```

### 2. **Run the App**
```bash
python app.py
```

### 3. **Navigate to "🖥️ Desktop Screen Capture" Tab**

### 4. **Configure Settings**
- Set target location coordinates
- Choose search radius (larger = more satellite tiles to compare)
- Select algorithm (basic = faster, enhanced = more accurate)
- Pick comparison method

### 5. **Start Recording**
- Click "⏹️ Start Recording Desktop"
- The app will begin capturing your screen
- Desktop feed appears in the left panel
- Stats update in the right panel

### 6. **Monitor Results**
- **FPS** - Frames processed per second
- **Frames Captured** - Total screenshots taken
- **Similarity Score** - How well each frame matches satellite data

### 7. **Stop Recording**
- Click "⏹️ Stop Recording" when done

## Performance Notes

- **FPS**: ~30 frames per second capture rate
- **Processing**: Every 3rd frame is analyzed (reduces CPU load)
- **GPU Acceleration**: Uses CUDA if available, falls back to CPU
- **Desktop Resolution**: Auto-resizes to 640x480 for faster processing

## Technical Details

### Capture Loop (Runs in Background Thread)
1. Take screenshot using `pyautogui.screenshot()`
2. Skip 2 frames, analyze every 3rd frame
3. Resize to 640x480 for speed
4. Extract embedding using ResNet50
5. Compare against satellite tile
6. Store results in global stats
7. Limit to ~30 FPS with small sleep interval

### Comparison Process
1. Get satellite tile for target coordinates
2. Extract features from both images using ResNet50
3. Calculate similarity using selected method (cosine, enhanced, SSIM, etc.)
4. Store score (0.0 = no match, 1.0 = perfect match)
5. Display in stats panel

## Troubleshooting

### "pyautogui not installed"
```bash
pip install pyautogui==0.9.53
```

### Screen Capture Not Working
- Make sure app has screen capture permissions (macOS may require permission)
- Check Desktop Screen Capture is enabled in System Preferences → Security & Privacy

### Low FPS
- Close other applications to free up CPU
- The app processes every 3rd frame by design - this is normal
- You can modify `frame_skip = 3` in the code to skip more frames if needed

### Poor Similarity Scores
- Adjust search radius (larger radius = more tiles to search)
- Try different comparison methods
- Use "Enhanced" algorithm for more accurate embeddings

## Files Modified

1. **app.py**
   - Added pyautogui import
   - Added desktop capture module (functions + globals)
   - Replaced streaming tab with desktop capture UI

2. **requirements.txt**
   - Added `pyautogui==0.9.53`

## Next Steps

You can now:
- ✅ Capture your desktop in real-time
- ✅ Compare it against satellite imagery
- ✅ Adjust search areas and algorithms
- ✅ Monitor FPS and similarity scores
- ⚠️ Add RTMP streaming if needed (separate module)
- ⚠️ Add video file export (save recordings)
- ⚠️ Add motion detection (alert on high similarity)

Enjoy desktop streaming! 🚀
