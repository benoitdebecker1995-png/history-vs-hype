@echo off
echo ================================================================================
echo FFmpeg Quick Installer for History Clip Tool
echo ================================================================================
echo.
echo This script will attempt to install FFmpeg using available package managers.
echo.
echo Trying winget first...
echo.

winget install --id=Gyan.FFmpeg -e --silent

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================================================
    echo SUCCESS! FFmpeg installed via winget
    echo ================================================================================
    echo.
    echo Please RESTART your terminal, then verify with: ffmpeg -version
    echo.
    pause
    exit /b 0
)

echo.
echo winget not available or failed. Trying chocolatey...
echo.

choco install ffmpeg -y

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================================================
    echo SUCCESS! FFmpeg installed via chocolatey
    echo ================================================================================
    echo.
    echo Please RESTART your terminal, then verify with: ffmpeg -version
    echo.
    pause
    exit /b 0
)

echo.
echo ================================================================================
echo Automatic installation failed.
echo ================================================================================
echo.
echo Please use one of these options:
echo.
echo Option 1: Run portable setup (no admin needed)
echo    python setup_ffmpeg_portable.py
echo.
echo Option 2: Manual download
echo    1. Go to: https://www.gyan.dev/ffmpeg/builds/
echo    2. Download: ffmpeg-release-essentials.zip
echo    3. Extract to: C:\ffmpeg\
echo    4. Add to PATH: C:\ffmpeg\bin
echo.
echo See INSTALL-FFMPEG.md for detailed instructions.
echo.
pause
