# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for History Clip Tool
Bundles Python runtime, dependencies, and all assets into a single executable.
"""

import sys
from pathlib import Path

block_cipher = None

# Determine platform
is_windows = sys.platform == 'win32'
is_macos = sys.platform == 'darwin'

# Base directory
base_dir = Path('.')

# Collect all source files
src_files = []
for pattern in ['**/*.py']:
    for file in (base_dir / 'src').rglob(pattern):
        src_files.append((str(file), str(file.parent.relative_to(base_dir))))

# Data files to include
datas = [
    # Configuration files (MUST be included)
    ('config/scoring_rules.toml', 'config'),
    ('config/caption_presets.toml', 'config'),

    # Frontend files
    ('frontend/public', 'frontend/public'),

    # Include source as data (for FastAPI to import)
    ('src', 'src'),
]

# Hidden imports (modules not auto-detected by PyInstaller)
hiddenimports = [
    'uvicorn.logging',
    'uvicorn.loops',
    'uvicorn.loops.auto',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.websockets',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.lifespan',
    'uvicorn.lifespan.on',
    'fastapi',
    'starlette',
    'pydantic',
    'sqlalchemy',
    'sqlalchemy.ext.declarative',
    'faster_whisper',
    'ffmpeg',
    'webview',
    'multiprocessing',
]

# Binaries (FFmpeg if bundled)
binaries = []

# On Windows, we can bundle FFmpeg
if is_windows:
    # Look for FFmpeg in common locations
    # User should download ffmpeg.exe and place it in the project root
    ffmpeg_path = base_dir / 'ffmpeg.exe'
    if ffmpeg_path.exists():
        binaries.append(('ffmpeg.exe', '.'))
    else:
        print("WARNING: ffmpeg.exe not found in project root.")
        print("Download from: https://www.gyan.dev/ffmpeg/builds/")
        print("Extract ffmpeg.exe to the project root for bundling.")

# Analysis
a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy.distutils',
        'scipy',
        'pandas',
        'PIL',
        'tkinter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# PYZ (compressed archive)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# EXE
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='HistoryClipTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if is_windows else 'icon.icns',  # Optional: add icon
)

# COLLECT (bundle everything into dist folder)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='HistoryClipTool',
)

# On macOS, create .app bundle
if is_macos:
    app = BUNDLE(
        coll,
        name='HistoryClipTool.app',
        icon='icon.icns',  # Optional
        bundle_identifier='com.historyvshype.cliptool',
        info_plist={
            'NSPrincipalClass': 'NSApplication',
            'NSHighResolutionCapable': 'True',
        },
    )
