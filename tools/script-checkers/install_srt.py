"""Install srt library if not already present."""
import subprocess
import sys

try:
    import srt
    print(f"srt already installed, version: {srt.__version__}")
except ImportError:
    print("Installing srt library...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "srt"])
    print("srt installed successfully")
