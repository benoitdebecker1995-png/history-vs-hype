#!/usr/bin/env python3
"""
Build script for History Clip Tool executable.
Automates the PyInstaller build process.
"""

import sys
import os
import shutil
import subprocess
from pathlib import Path

# Platform detection
IS_WINDOWS = sys.platform == 'win32'
IS_MACOS = sys.platform == 'darwin'
IS_LINUX = sys.platform.startswith('linux')

# Directories
BASE_DIR = Path(__file__).parent
DIST_DIR = BASE_DIR / 'dist'
BUILD_DIR = BASE_DIR / 'build'
SPEC_FILE = BASE_DIR / 'history-clip-tool.spec'


def print_header(message):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f"  {message}")
    print("="*60 + "\n")


def check_dependencies():
    """Check if all build dependencies are installed."""
    print_header("Checking Build Dependencies")

    missing = []

    # Check Python version
    if sys.version_info < (3, 10):
        print("❌ Python 3.10+ required")
        missing.append("Python 3.10+")
    else:
        print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}")

    # Check PyInstaller
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller not installed")
        missing.append("PyInstaller")

    # Check other dependencies
    deps = ['fastapi', 'uvicorn', 'webview', 'ffmpeg']
    for dep in deps:
        try:
            __import__(dep.replace('-', '_'))
            print(f"✓ {dep}")
        except ImportError:
            print(f"❌ {dep} not installed")
            missing.append(dep)

    if missing:
        print("\nMissing dependencies:")
        for dep in missing:
            print(f"  - {dep}")
        print("\nInstall with:")
        print("  pip install -r requirements.txt")
        print("  pip install pyinstaller")
        return False

    return True


def check_ffmpeg():
    """Check if FFmpeg is available for bundling (Windows only)."""
    if IS_WINDOWS:
        print_header("Checking FFmpeg for Bundling")

        ffmpeg_exe = BASE_DIR / 'ffmpeg.exe'
        if ffmpeg_exe.exists():
            print(f"✓ FFmpeg found: {ffmpeg_exe}")
            return True
        else:
            print("⚠ FFmpeg not found in project root")
            print("\nFFmpeg will NOT be bundled with the executable.")
            print("Users will need to install FFmpeg separately.")
            print("\nTo bundle FFmpeg:")
            print("  1. Download from: https://www.gyan.dev/ffmpeg/builds/")
            print("  2. Extract ffmpeg.exe")
            print("  3. Copy ffmpeg.exe to:", BASE_DIR)
            print("  4. Re-run this build script")
            return False
    else:
        print("FFmpeg bundling not needed on macOS/Linux (system FFmpeg will be used)")
        return True


def clean_build():
    """Clean previous build artifacts."""
    print_header("Cleaning Previous Build")

    dirs_to_clean = [BUILD_DIR, DIST_DIR]

    for dir_path in dirs_to_clean:
        if dir_path.exists():
            print(f"Removing {dir_path}...")
            shutil.rmtree(dir_path)
            print(f"✓ Cleaned {dir_path}")

    print("✓ Build environment cleaned")


def run_pyinstaller():
    """Run PyInstaller with spec file."""
    print_header("Building Executable")

    if not SPEC_FILE.exists():
        print(f"❌ Spec file not found: {SPEC_FILE}")
        return False

    # Run PyInstaller
    cmd = ['pyinstaller', '--clean', str(SPEC_FILE)]

    print(f"Running: {' '.join(cmd)}")
    print()

    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("\n✓ Build completed successfully")
        return True
    else:
        print("\n❌ Build failed")
        return False


def verify_build():
    """Verify that build output exists."""
    print_header("Verifying Build Output")

    if IS_WINDOWS:
        exe_path = DIST_DIR / 'HistoryClipTool' / 'HistoryClipTool.exe'
    elif IS_MACOS:
        exe_path = DIST_DIR / 'HistoryClipTool.app'
    else:
        exe_path = DIST_DIR / 'HistoryClipTool' / 'HistoryClipTool'

    if exe_path.exists():
        print(f"✓ Executable found: {exe_path}")

        # Check size
        if IS_MACOS:
            # For .app bundle, check the actual executable inside
            actual_exe = exe_path / 'Contents' / 'MacOS' / 'HistoryClipTool'
            if actual_exe.exists():
                size_mb = actual_exe.stat().st_size / (1024 * 1024)
            else:
                size_mb = 0
        else:
            size_mb = exe_path.stat().st_size / (1024 * 1024)

        print(f"  Size: {size_mb:.1f} MB")
        return True
    else:
        print(f"❌ Executable not found: {exe_path}")
        return False


def create_dist_package():
    """Create distribution package with README."""
    print_header("Creating Distribution Package")

    # Create README for users
    readme_content = """# History Clip Tool

## How to Use

1. **First Time Setup:**
   - Ensure FFmpeg is installed on your system
   - Windows: Download from https://ffmpeg.org
   - macOS: Install with `brew install ffmpeg`

2. **Running the App:**
   - Double-click HistoryClipTool.exe (Windows) or HistoryClipTool.app (macOS)
   - The app will open in a new window
   - No terminal or command line needed

3. **First Run:**
   - The app will set up data directories
   - Whisper models will download automatically when you first transcribe
   - This may take a few minutes

4. **Using the Tool:**
   - Upload a video
   - Transcribe it
   - Review suggested clips
   - Export selected clips

## Data Storage

All your data is stored locally in the same folder as the app:
- `data/` - Your projects and clips
- `models/` - Downloaded Whisper models
- `logs/` - Processing logs

## Troubleshooting

**"FFmpeg not found"**
- Install FFmpeg from https://ffmpeg.org
- Restart the application

**App won't start**
- Check that port 8000 is not in use
- Try running as administrator (Windows) or with appropriate permissions

**Slow transcription**
- This is normal - transcription runs on your CPU
- Use "Fast" mode for quicker results

## Privacy

This tool runs 100% locally. No data leaves your computer.
No cloud services. No analytics. No accounts.

## Support

For issues, check the logs in the `logs/` folder.
"""

    dist_folder = DIST_DIR / 'HistoryClipTool'

    if dist_folder.exists():
        readme_path = dist_folder / 'README.txt'
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        print(f"✓ Created README: {readme_path}")
    else:
        print("⚠ Distribution folder not found, skipping README")


def print_success_message():
    """Print final success message with instructions."""
    print_header("Build Complete!")

    if IS_WINDOWS:
        exe_path = DIST_DIR / 'HistoryClipTool' / 'HistoryClipTool.exe'
        print("Executable location:")
        print(f"  {exe_path.absolute()}")
        print("\nTo distribute:")
        print(f"  1. Zip the entire folder: {DIST_DIR / 'HistoryClipTool'}")
        print("  2. Share the zip file")
        print("  3. Users extract and double-click HistoryClipTool.exe")

    elif IS_MACOS:
        app_path = DIST_DIR / 'HistoryClipTool.app'
        print("Application bundle:")
        print(f"  {app_path.absolute()}")
        print("\nTo distribute:")
        print("  1. Zip HistoryClipTool.app")
        print("  2. Share the zip file")
        print("  3. Users extract and double-click HistoryClipTool.app")

    else:
        exe_path = DIST_DIR / 'HistoryClipTool' / 'HistoryClipTool'
        print("Executable location:")
        print(f"  {exe_path.absolute()}")
        print("\nTo distribute:")
        print(f"  1. Tar/zip the folder: {DIST_DIR / 'HistoryClipTool'}")
        print("  2. Share the archive")
        print("  3. Users extract and run ./HistoryClipTool")

    print("\n⚠ Important:")
    print("  - Users must have FFmpeg installed")
    print("  - First run will download Whisper models (~150MB for base model)")
    print("  - All processing is local - no internet needed after setup")


def main():
    """Main build process."""
    print_header("History Clip Tool - Build Script")

    # Step 1: Check dependencies
    if not check_dependencies():
        print("\n❌ Build cannot proceed - missing dependencies")
        return 1

    # Step 2: Check FFmpeg
    check_ffmpeg()  # Warning only, not fatal

    # Step 3: Clean
    clean_build()

    # Step 4: Build
    if not run_pyinstaller():
        print("\n❌ Build failed")
        return 1

    # Step 5: Verify
    if not verify_build():
        print("\n❌ Build verification failed")
        return 1

    # Step 6: Create distribution package
    create_dist_package()

    # Step 7: Success
    print_success_message()

    return 0


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
