# Build Instructions for History Clip Tool

Complete guide to building a standalone executable that users can launch by double-clicking.

## Prerequisites

### All Platforms

1. **Python 3.10+**
   - Windows: Download from python.org
   - macOS: `brew install python@3.10`
   - Linux: `sudo apt install python3.10`

2. **FFmpeg** (for testing the build)
   - Windows: Download from https://ffmpeg.org/download.html
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

### Platform-Specific

**Windows:**
- Visual Studio Build Tools (for some Python packages)
- Download from: https://visualstudio.microsoft.com/downloads/

**macOS:**
- Xcode Command Line Tools: `xcode-select --install`

**Linux:**
- Build essentials: `sudo apt install build-essential`

---

## Step 1: Set Up Development Environment

### Clone/Navigate to Project

```bash
cd tools/history-clip-tool
```

### Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs:
- All runtime dependencies (FastAPI, faster-whisper, etc.)
- pywebview (for native GUI window)
- pyinstaller (for building executable)

---

## Step 2: Test the Application

Before building, verify everything works:

```bash
python launcher.py
```

This should:
1. Start the backend server
2. Open a native window with the UI
3. Allow you to upload a video and test the workflow

**Important:** Test thoroughly in launcher mode before building the executable.

Close the window when done testing.

---

## Step 3: Prepare for Building

### Windows: Bundle FFmpeg (Optional but Recommended)

To bundle FFmpeg with the Windows executable:

1. Download FFmpeg static build:
   - Go to: https://www.gyan.dev/ffmpeg/builds/
   - Download: `ffmpeg-release-essentials.zip`

2. Extract `ffmpeg.exe`:
   - Open the zip file
   - Navigate to `bin/` folder
   - Copy `ffmpeg.exe`

3. Place in project root:
   ```
   tools/history-clip-tool/ffmpeg.exe
   ```

If you skip this, Windows users will need to install FFmpeg separately.

### macOS/Linux: System FFmpeg

On macOS and Linux, the executable will use the system's FFmpeg installation. Users must have FFmpeg installed via Homebrew or apt.

---

## Step 4: Build the Executable

### Run Build Script

```bash
python build.py
```

The script will:
1. ✓ Check all dependencies are installed
2. ✓ Check if FFmpeg is available for bundling (Windows)
3. ✓ Clean previous build artifacts
4. ✓ Run PyInstaller with the spec file
5. ✓ Verify the build output
6. ✓ Create distribution package with README

**Build time:** 5-10 minutes (first build downloads dependencies)

### Build Output

**Windows:**
```
dist/HistoryClipTool/
├── HistoryClipTool.exe          # Main executable
├── _internal/                   # Bundled dependencies
├── data/                        # Created on first run
├── models/                      # Created on first run
└── README.txt                   # User instructions
```

**macOS:**
```
dist/
└── HistoryClipTool.app/         # Application bundle
    └── Contents/
        ├── MacOS/
        │   └── HistoryClipTool  # Executable
        ├── Resources/           # Bundled files
        └── Info.plist
```

**Linux:**
```
dist/HistoryClipTool/
├── HistoryClipTool              # Executable
├── _internal/                   # Bundled dependencies
└── README.txt
```

---

## Step 5: Test the Executable

### Windows

1. Navigate to `dist/HistoryClipTool/`
2. Double-click `HistoryClipTool.exe`
3. The app should open in a new window (no terminal)

### macOS

1. Navigate to `dist/`
2. Double-click `HistoryClipTool.app`
3. If macOS blocks it (unidentified developer):
   - Right-click → Open
   - Click "Open" in the security dialog

### Linux

1. Navigate to `dist/HistoryClipTool/`
2. Make executable: `chmod +x HistoryClipTool`
3. Run: `./HistoryClipTool`

### First Run Behavior

On first launch:
1. ✓ Creates `data/`, `models/`, `logs/` directories
2. ✓ Shows first-run setup screen
3. ✓ Checks for FFmpeg
4. ✓ Opens main application window

On subsequent launches:
- Skips setup
- Opens directly to main window

### Test Checklist

- [ ] App opens without terminal window
- [ ] FFmpeg check passes (or shows clear error)
- [ ] Can upload a video
- [ ] Transcription starts (downloads model on first use)
- [ ] Clips are detected
- [ ] Clips can be exported
- [ ] Exported clips play correctly
- [ ] Window closes cleanly

---

## Step 6: Distribute to Users

### Windows Distribution

**Option A: Zip File (Recommended)**

```bash
# From dist/ folder
cd dist
# Zip the entire folder
Compress-Archive -Path HistoryClipTool -DestinationPath HistoryClipTool-Windows.zip
```

Users:
1. Download `HistoryClipTool-Windows.zip`
2. Extract to any folder
3. Double-click `HistoryClipTool.exe`

**Option B: Installer (Advanced)**

Use Inno Setup or NSIS to create a proper installer.

### macOS Distribution

**Option A: Zip App Bundle**

```bash
cd dist
zip -r HistoryClipTool-macOS.zip HistoryClipTool.app
```

Users:
1. Download `HistoryClipTool-macOS.zip`
2. Extract `HistoryClipTool.app`
3. Move to Applications folder (optional)
4. Double-click to run

**Option B: DMG Image (Advanced)**

Use `create-dmg` or `appdmg` to create a DMG installer.

**Important for macOS:**
- The app is not code-signed, so users must right-click → Open the first time
- For production, you should sign with an Apple Developer certificate

### Linux Distribution

**Tar.gz Archive**

```bash
cd dist
tar -czf HistoryClipTool-Linux.tar.gz HistoryClipTool/
```

Users:
1. Download `HistoryClipTool-Linux.tar.gz`
2. Extract: `tar -xzf HistoryClipTool-Linux.tar.gz`
3. Run: `./HistoryClipTool/HistoryClipTool`

---

## Troubleshooting Build Issues

### "ModuleNotFoundError" during build

**Problem:** PyInstaller can't find a module

**Solution:**
1. Add missing module to `hiddenimports` in `history-clip-tool.spec`
2. Rebuild: `python build.py`

### "Permission denied" on macOS

**Problem:** Can't execute the app

**Solution:**
```bash
chmod +x dist/HistoryClipTool.app/Contents/MacOS/HistoryClipTool
```

### Executable is very large (>500MB)

**Normal.** The executable includes:
- Python runtime (~50MB)
- PyTorch for Whisper (~300MB)
- All dependencies

This is unavoidable for a standalone executable with ML capabilities.

### "FFmpeg not found" when running

**Windows:**
- Bundle `ffmpeg.exe` in project root before building
- Or tell users to install FFmpeg separately

**macOS/Linux:**
- Users must install FFmpeg: `brew install ffmpeg` or `sudo apt install ffmpeg`

### Build works but app won't start

**Check:**
1. Port 8000 is not already in use
2. Antivirus isn't blocking the executable
3. Look for error logs in `logs/` folder (created in app directory)

### "Failed to execute script launcher"

**Problem:** PyInstaller hook missing for a dependency

**Solution:**
1. Run with debug: `pyinstaller --debug=all history-clip-tool.spec`
2. Check error message
3. Add missing hooks to spec file

---

## Advanced: Customizing the Build

### Change Application Name

Edit `history-clip-tool.spec`:

```python
exe = EXE(
    ...
    name='MyCustomName',  # Change this
    ...
)
```

### Add Application Icon

1. Create icon files:
   - Windows: `icon.ico` (256x256)
   - macOS: `icon.icns` (512x512)

2. Place in project root

3. Icon will be automatically included (already configured in spec file)

### Reduce Executable Size

Edit `history-clip-tool.spec`:

```python
excludes=[
    'matplotlib',      # Already excluded
    'numpy.distutils', # Already excluded
    'scipy',           # Already excluded
    'pandas',          # Already excluded
    # Add more unused packages here
],
```

### Enable Debug Console (for troubleshooting)

Edit `history-clip-tool.spec`:

```python
exe = EXE(
    ...
    console=True,  # Change from False to True
    ...
)
```

Rebuild. The executable will now show a console window with debug output.

---

## Build Checklist

Before distributing to users:

- [ ] Tested in launcher mode (`python launcher.py`)
- [ ] All features working (upload, transcribe, detect, export)
- [ ] Build completes without errors (`python build.py`)
- [ ] Executable runs without terminal window
- [ ] FFmpeg detection works or shows clear error message
- [ ] First-run setup displays correctly
- [ ] Model download works on first transcription
- [ ] Exported clips are valid video files
- [ ] README.txt included in distribution
- [ ] Tested on clean system (no Python installed)

---

## File Size Reference

**Expected sizes:**

| Platform | Compressed (zip) | Uncompressed |
|----------|-----------------|--------------|
| Windows  | ~180 MB         | ~450 MB      |
| macOS    | ~200 MB         | ~500 MB      |
| Linux    | ~190 MB         | ~480 MB      |

**After first use (with Whisper base model):**
- Add ~150 MB for downloaded model

**With user projects:**
- Depends on video size and number of projects

---

## User System Requirements

Distribute this with your executable:

**Minimum:**
- OS: Windows 10+, macOS 11+, Ubuntu 20.04+
- CPU: Dual-core 2.0 GHz
- RAM: 4 GB
- Storage: 2 GB free (more for videos and models)
- FFmpeg installed separately (unless bundled on Windows)

**Recommended:**
- OS: Windows 11, macOS 12+, Ubuntu 22.04+
- CPU: Quad-core 2.5 GHz+
- RAM: 8 GB+
- Storage: 10 GB+ free
- SSD for faster transcription

---

## Support Resources

For users experiencing issues:

1. **Check README.txt** in distribution folder
2. **Check logs** in `logs/` folder (created next to executable)
3. **Verify FFmpeg**: Run `ffmpeg -version` in terminal
4. **Antivirus**: Whitelist the executable if blocked
5. **Port conflict**: Close apps using port 8000

---

## Next Steps

After successful build:

1. **Test on clean machine** (VM recommended)
2. **Create release notes** documenting features
3. **Package with clear instructions** for non-technical users
4. **Consider code signing** for macOS/Windows (production)
5. **Set up update mechanism** (for future versions)

---

## Questions?

Common issues and solutions documented above. For build-specific problems:
- Check PyInstaller documentation: https://pyinstaller.org
- Check pywebview issues: https://github.com/r0x0r/pywebview

**Remember:** The goal is a double-click experience. Test on non-technical users before public release.
