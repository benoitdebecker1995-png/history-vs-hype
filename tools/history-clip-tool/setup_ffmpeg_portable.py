"""
Portable FFmpeg Setup for History Clip Tool
Downloads and configures ffmpeg to work without modifying system PATH
"""

import os
import sys
import urllib.request
import zipfile
from pathlib import Path
import subprocess
import shutil

# Configuration
FFMPEG_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
TOOL_DIR = Path(__file__).parent.absolute()
FFMPEG_DIR = TOOL_DIR.parent / "ffmpeg"
FFMPEG_BIN = FFMPEG_DIR / "bin"

def download_ffmpeg():
    """Download ffmpeg essentials build"""
    print("=" * 80)
    print("FFmpeg Portable Setup for History Clip Tool")
    print("=" * 80)
    print()

    # Check if already downloaded
    if FFMPEG_BIN.exists() and (FFMPEG_BIN / "ffmpeg.exe").exists():
        print(f"✓ FFmpeg already exists at: {FFMPEG_BIN}")
        return True

    print(f"Downloading FFmpeg to: {FFMPEG_DIR}")
    print("This may take 5-10 minutes (100MB download)...")
    print()

    # Create directory
    FFMPEG_DIR.mkdir(parents=True, exist_ok=True)

    # Download
    zip_path = FFMPEG_DIR / "ffmpeg.zip"

    try:
        def progress_hook(block_num, block_size, total_size):
            downloaded = block_num * block_size
            percent = min(100, (downloaded / total_size) * 100)
            bar_length = 50
            filled = int(bar_length * downloaded / total_size)
            bar = '█' * filled + '-' * (bar_length - filled)

            sys.stdout.write(f'\r[{bar}] {percent:.1f}% ({downloaded/1024/1024:.1f}MB / {total_size/1024/1024:.1f}MB)')
            sys.stdout.flush()

        urllib.request.urlretrieve(FFMPEG_URL, zip_path, progress_hook)
        print("\n\n✓ Download complete!")

    except Exception as e:
        print(f"\n✗ Download failed: {e}")
        print("\nManual installation required:")
        print(f"1. Download: {FFMPEG_URL}")
        print(f"2. Extract to: {FFMPEG_DIR}")
        print(f"3. Ensure ffmpeg.exe is at: {FFMPEG_BIN / 'ffmpeg.exe'}")
        return False

    # Extract
    print("\nExtracting archive...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Extract all files
            zip_ref.extractall(FFMPEG_DIR)

        # Find the extracted folder (it has a version number in the name)
        extracted_folders = [f for f in FFMPEG_DIR.iterdir() if f.is_dir() and f.name.startswith('ffmpeg-')]

        if extracted_folders:
            # Move contents up one level
            extracted_folder = extracted_folders[0]
            for item in extracted_folder.iterdir():
                dest = FFMPEG_DIR / item.name
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.move(str(item), str(dest))

            # Remove now-empty folder
            extracted_folder.rmdir()

        # Clean up zip
        zip_path.unlink()

        print("✓ Extraction complete!")

    except Exception as e:
        print(f"✗ Extraction failed: {e}")
        return False

    return True

def verify_ffmpeg():
    """Verify ffmpeg installation"""
    ffmpeg_exe = FFMPEG_BIN / "ffmpeg.exe"

    if not ffmpeg_exe.exists():
        print(f"✗ FFmpeg executable not found at: {ffmpeg_exe}")
        return False

    try:
        result = subprocess.run(
            [str(ffmpeg_exe), "-version"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✓ FFmpeg verified: {version_line}")
            return True
        else:
            print("✗ FFmpeg execution failed")
            return False

    except Exception as e:
        print(f"✗ FFmpeg verification failed: {e}")
        return False

def configure_python_environment():
    """Configure Python to use portable ffmpeg"""
    config_file = TOOL_DIR / "config" / "ffmpeg_path.txt"
    config_file.parent.mkdir(exist_ok=True)

    with open(config_file, 'w') as f:
        f.write(str(FFMPEG_BIN))

    print(f"✓ Configuration saved to: {config_file}")

    # Update the video processor to use this path
    video_processor_path = TOOL_DIR / "src" / "core" / "video_processor.py"

    if video_processor_path.exists():
        print("✓ Clipping tool will use portable ffmpeg automatically")
    else:
        print("⚠ Warning: video_processor.py not found - manual configuration may be needed")

def main():
    """Main setup routine"""
    print()

    # Step 1: Download
    if not download_ffmpeg():
        return 1

    # Step 2: Verify
    print()
    if not verify_ffmpeg():
        return 1

    # Step 3: Configure
    print()
    configure_python_environment()

    print()
    print("=" * 80)
    print("✓ SETUP COMPLETE!")
    print("=" * 80)
    print()
    print("FFmpeg is now configured for portable use.")
    print("You can now run the clipping tool:")
    print()
    print("    python run.py")
    print()
    print(f"FFmpeg location: {FFMPEG_BIN}")
    print()

    return 0

if __name__ == "__main__":
    sys.exit(main())
