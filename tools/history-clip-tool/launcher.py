#!/usr/bin/env python3
"""
History Clip Tool Launcher
Starts backend and opens UI in a native window.
No terminal required.
"""

import sys
import os
import threading
import time
import signal
import subprocess
from pathlib import Path
import multiprocessing

# Ensure we're in the correct directory
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    BASE_DIR = Path(sys._MEIPASS)
    APP_DIR = Path(os.path.dirname(sys.executable))
else:
    # Running as script
    BASE_DIR = Path(__file__).parent
    APP_DIR = BASE_DIR

# Add src to path
sys.path.insert(0, str(BASE_DIR / "src"))

import uvicorn
import webview


# Global server instance for cleanup
server = None
server_thread = None


class ServerThread(threading.Thread):
    """Background thread to run FastAPI server."""

    def __init__(self, app_dir):
        super().__init__(daemon=True)
        self.app_dir = app_dir
        self.should_stop = False

    def run(self):
        """Start uvicorn server."""
        # Set up data directories in app directory (persistent across runs)
        os.environ['APP_DATA_DIR'] = str(self.app_dir / 'data')
        os.environ['APP_MODELS_DIR'] = str(self.app_dir / 'models')
        os.environ['APP_LOGS_DIR'] = str(self.app_dir / 'logs')

        # Ensure directories exist
        (self.app_dir / 'data').mkdir(exist_ok=True)
        (self.app_dir / 'models').mkdir(exist_ok=True)
        (self.app_dir / 'logs').mkdir(exist_ok=True)

        # Start server
        config = uvicorn.Config(
            "api.main:app",
            host="127.0.0.1",
            port=8000,
            log_level="error",  # Suppress console output
            access_log=False
        )
        global server
        server = uvicorn.Server(config)
        server.run()

    def stop(self):
        """Stop the server gracefully."""
        self.should_stop = True
        if server:
            server.should_exit = True


def check_ffmpeg():
    """
    Check if FFmpeg is available.
    Returns True if found, False otherwise.
    """
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def check_first_run():
    """Check if this is the first run."""
    marker_file = APP_DIR / 'data' / '.initialized'
    return not marker_file.exists()


def create_first_run_marker():
    """Create marker file to indicate setup is complete."""
    marker_file = APP_DIR / 'data' / '.initialized'
    marker_file.parent.mkdir(parents=True, exist_ok=True)
    marker_file.touch()


def wait_for_server(max_attempts=30):
    """
    Wait for server to be ready.

    Args:
        max_attempts: Maximum number of connection attempts

    Returns:
        True if server is ready, False if timeout
    """
    import socket

    for i in range(max_attempts):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', 8000))
            sock.close()

            if result == 0:
                return True
        except OSError:
            pass

        time.sleep(0.5)

    return False


def on_window_closing():
    """Handle window close event."""
    # Stop the server
    if server_thread:
        server_thread.stop()

    # Give it a moment to clean up
    time.sleep(0.5)


def show_error_dialog(title, message):
    """Show error message in a dialog."""
    webview.create_window(
        title,
        html=f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    margin: 0;
                    background: #f5f5f5;
                }}
                .error {{
                    background: white;
                    padding: 40px;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    max-width: 500px;
                    text-align: center;
                }}
                h1 {{
                    color: #d32f2f;
                    margin-bottom: 20px;
                }}
                p {{
                    color: #555;
                    line-height: 1.6;
                }}
            </style>
        </head>
        <body>
            <div class="error">
                <h1>⚠️ {title}</h1>
                <p>{message}</p>
            </div>
        </body>
        </html>
        """,
        width=600,
        height=300
    )
    webview.start()


def show_first_run_setup():
    """Show first-run setup window."""
    setup_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            .setup {
                background: white;
                padding: 50px;
                border-radius: 12px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.2);
                max-width: 600px;
                text-align: center;
            }
            h1 {
                color: #1a1a1a;
                margin-bottom: 15px;
            }
            .subtitle {
                color: #666;
                margin-bottom: 30px;
                font-size: 18px;
            }
            .status {
                background: #f0f7ff;
                border-left: 4px solid #2563eb;
                padding: 20px;
                margin: 20px 0;
                text-align: left;
            }
            .check {
                margin: 10px 0;
                color: #059669;
            }
            .spinner {
                display: inline-block;
                width: 20px;
                height: 20px;
                border: 3px solid #f3f3f3;
                border-top: 3px solid #2563eb;
                border-radius: 50%;
                animation: spin 1s linear infinite;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            #continue-btn {
                background: #2563eb;
                color: white;
                border: none;
                padding: 15px 40px;
                border-radius: 6px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                display: none;
            }
            #continue-btn:hover {
                background: #1d4ed8;
            }
        </style>
    </head>
    <body>
        <div class="setup">
            <h1>Welcome to History Clip Tool</h1>
            <p class="subtitle">Local video clipping for historical content</p>

            <div class="status">
                <div id="status-message">
                    <div class="spinner"></div> Setting up for first use...
                </div>
            </div>

            <button id="continue-btn" onclick="window.location.reload()">
                Continue to App
            </button>
        </div>

        <script>
            // Simulate setup checks
            setTimeout(() => {
                document.getElementById('status-message').innerHTML =
                    '<div class="check">✓ Created data directories</div>' +
                    '<div class="check">✓ Server is running</div>' +
                    '<div class="check">✓ Ready to use</div>';
                document.getElementById('continue-btn').style.display = 'inline-block';
            }, 2000);
        </script>
    </body>
    </html>
    """

    window = webview.create_window(
        'History Clip Tool - First Run Setup',
        html=setup_html,
        width=700,
        height=500
    )

    webview.start()


def main():
    """Main entry point."""
    global server_thread

    # Check for FFmpeg
    if not check_ffmpeg():
        show_error_dialog(
            "FFmpeg Not Found",
            "FFmpeg is required but not installed.<br><br>"
            "Please install FFmpeg:<br>"
            "Windows: Download from ffmpeg.org<br>"
            "macOS: brew install ffmpeg<br><br>"
            "Then restart this application."
        )
        return

    # Show first-run setup if needed
    first_run = check_first_run()

    # Start backend server
    server_thread = ServerThread(APP_DIR)
    server_thread.start()

    # Wait for server to be ready
    if not wait_for_server():
        show_error_dialog(
            "Server Failed to Start",
            "The backend server could not start.<br><br>"
            "Please check that port 8000 is available."
        )
        return

    # Show first-run setup or main app
    if first_run:
        create_first_run_marker()
        show_first_run_setup()
        # After setup window closes, open main app

    # Create main application window
    window = webview.create_window(
        'History Clip Tool',
        'http://127.0.0.1:8000',
        width=1400,
        height=900,
        resizable=True,
        background_color='#fafafa'
    )

    # Set up close handler
    window.events.closing += on_window_closing

    # Start the UI
    webview.start()

    # Clean shutdown
    if server_thread:
        server_thread.stop()


if __name__ == '__main__':
    # Prevent multiple instances on Windows
    if sys.platform == 'win32':
        # This ensures PyInstaller bundles work correctly
        multiprocessing.freeze_support()

    main()
