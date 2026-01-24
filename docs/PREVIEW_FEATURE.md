# Preview Feature Documentation

## Overview

The Badge Generator GUI now includes a **Preview Section** that displays sample images in real-time, providing instant visual feedback for badge generation operations.

## Features

### 1. Three-Panel Preview Display
The preview section shows three images side-by-side:

| Panel | Source | Updates When |
|-------|--------|--------------|
| **Template** | Badge template file | App starts, config saved |
| **Source** | First image from source folder | App starts, new images pulled, config saved |
| **Output** | First generated badge | Badges are generated, cleanup removes it |

### 2. Auto-Refresh on Actions
Preview automatically updates when you click any action button:

| Button | Action | Preview Update |
|--------|--------|-----------------|
| **Generate** | Creates badges | Shows new generated badge |
| **Cleanup** | Deletes output | Shows "No Image" placeholder |
| **Pull Image** | Imports source images | Shows first newly pulled image |
| **Save Config** | Saves settings | Refreshes with current images |

### 3. Intelligent Image Detection
- Automatically finds images in configured directories
- Supports multiple formats: PNG, JPEG, BMP, WebP
- Handles missing images gracefully with "No Image" placeholder
- Works with both absolute and relative file paths

### 4. Responsive Display
- Images auto-scale to fill available space
- Maintains aspect ratio automatically
- Thumbnail size: up to 200×300 pixels
- Adjusts based on window size

## How It Works

### On Application Start
1. Preview section initializes with three panels
2. Loads template image
3. Loads first source image
4. Loads first output image (if it exists)

### During Operations
```
User clicks action button
    ↓
Action runs in background
    ↓
Action completes
    ↓
Preview refresh scheduled (500ms delay)
    ↓
Old cached images cleared
    ↓
New images loaded from disk
    ↓
Preview updates on main GUI thread
```

### Path Resolution
The system checks paths in this order:
1. Absolute paths (if configured)
2. Relative to package root (`badge_generator/badge_generator/`)
3. Relative to workspace root (`badge_generator/`)

This ensures compatibility with different folder structures.

## Configuration

### Image Directories (in `config.ini`)

```ini
[general]
src_path = images/source/src_img/        # Source images directory
des_path = images/output/des_img/        # Generated output directory

[template]
filename = images/templates/template_full.png  # Badge template
```

### UI Settings

```ini
[ui settings]
show_success = False   # Controls success message popups
show_error = True      # Controls error message popups
```

## GUI Layout

```
┌─────────────────────────────────────────────────┐
│  Badge Generator - Image Producer              │
├─────────────────────────────────────────────────┤
│  CONFIG SECTION          │  ACTION SECTION      │
│  ┌─────────────────────┐ │  [Generate]         │
│  │ Config settings     │ │  [Cleanup]          │
│  │ with friendly       │ │  [Pull Image]       │
│  │ labels and inputs   │ │  [Save Config]      │
│  │                     │ │  [Progress Bar]     │
│  └─────────────────────┘ │                     │
│                          │  PREVIEW SECTION    │
│                          │  ┌─────────────────┐│
│                          │  │ Template │ Source││ Output │
│                          │  │ ┌─────┐ ┌─────┐ ├─────┐
│                          │  │ │Image│ │Image│ │Image│
│                          │  │ └─────┘ └─────┘ └─────┘
│                          │  └─────────────────┘│
│                          │                     │
│                          │  TERMINAL SECTION   │
│                          │  ┌─────────────────┐│
│                          │  │ Command output  ││
│                          │  │ and messages    ││
│                          │  └─────────────────┘│
└─────────────────────────────────────────────────┘
```

## Terminal Output

When preview operations occur, you'll see debug messages in the terminal:

```
[Preview] Scheduling refresh...
[Preview] Loading images...
[Preview] Images loaded successfully
```

If there are issues:
```
[Preview] Refresh error: [error details]
[Preview] Error loading images: [error details]
```

## Technical Implementation

### Key Methods

#### `_load_preview_images()`
- Main method that loads all preview images
- Called automatically on app start
- Called on every action button refresh

#### `_clear_preview_images()`
- Clears cached images before loading new ones
- Prevents "stale image" bug after cleanup
- Allows garbage collection of old PhotoImages

#### `_display_image(preview_type, image_path)`
- Converts image to PIL thumbnail
- Displays in Tkinter label
- Maintains memory reference to prevent garbage collection

#### `_refresh_preview()`
- Thread-safe wrapper method
- Schedules refresh on main GUI thread
- 500ms delay for file system catch-up

### Dependencies

- **PIL/Pillow**: Image loading and conversion
  - Optional: App works without it but shows placeholders
  - Installation: `pip install Pillow`
- **Tkinter**: GUI display (built-in with Python)
- **pathlib**: File path handling

## Known Limitations

1. **First Image Only**: Preview shows the first image found (alphabetically sorted)
   - Future enhancement: Allow user to select which images to preview

2. **No Auto-Refresh on External Changes**: If files change outside the app, preview doesn't update
   - Workaround: Click any action button to manually refresh

3. **Placeholder Text Size**: Text may be cut off with very small window sizes
   - Workaround: Resize window larger

4. **PIL Dependency**: Image display requires Pillow
   - Fallback: Shows "No Image" placeholders without PIL

## Troubleshooting

### Preview Shows "No Image" for All Items

**Cause**: File paths in config.ini don't match actual file locations

**Solution**:
1. Check `config.ini` paths
2. Verify images exist in those directories
3. Use absolute paths if relative paths don't work

### Preview Doesn't Update After Action

**Cause**: Background operation hasn't completed yet

**Solution**:
1. Wait a moment (operations run in background)
2. Watch terminal for "[Preview]" messages
3. Manually click another button to force refresh

### Preview Shows Old Images After Cleanup

**Cause**: Image cache not cleared (should be fixed now)

**Solution**:
1. Update to latest version (cache clearing implemented)
2. Manually refresh by clicking Save Config

### PIL Not Found Error

**Cause**: Pillow package not installed

**Solution**:
```bash
pip install Pillow
```

Preview will work without it but show placeholders.

## Future Enhancements

Potential improvements for future versions:

- [ ] User-selectable preview images (not just first)
- [ ] Image info tooltips (filename, size, dimensions)
- [ ] Drag-drop image selection for preview
- [ ] Larger preview window (double-click to expand)
- [ ] Animated GIF support
- [ ] Preview refresh on external file changes
- [ ] Image comparison view (before/after)
- [ ] Batch preview display (multiple output images)

## Support & Questions

For issues or questions about the preview feature:

1. Check **Terminal Output** for "[Preview]" debug messages
2. Review **Troubleshooting** section above
3. Check `config.ini` paths are correct
4. Ensure PIL/Pillow is installed
5. Create a GitHub issue with details and logs

---

**Status**: ✅ Production Ready  
**Last Updated**: January 24, 2026  
**Tested On**: Windows 10/11, Python 3.8+  
