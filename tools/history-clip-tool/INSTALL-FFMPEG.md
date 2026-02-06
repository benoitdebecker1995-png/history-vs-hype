# FFmpeg Installation Guide for Windows

## Option 1: Quick Install with Chocolatey (Recommended)

If you have Chocolatey installed, open **PowerShell as Administrator** and run:

```powershell
choco install ffmpeg -y
```

Then restart your terminal and verify:
```bash
ffmpeg -version
```

## Option 2: Quick Install with winget

Open **PowerShell** or **Command Prompt** and run:

```powershell
winget install --id=Gyan.FFmpeg -e
```

Then restart your terminal and verify:
```bash
ffmpeg -version
```

## Option 3: Manual Installation (Works for sure)

1. **Download FFmpeg**
   - Go to: https://www.gyan.dev/ffmpeg/builds/
   - Download: `ffmpeg-release-essentials.zip` (about 100MB)

2. **Extract the Archive**
   - Right-click the ZIP file and select "Extract All"
   - Extract to: `C:\ffmpeg\`
   - You should have: `C:\ffmpeg\bin\ffmpeg.exe`

3. **Add to PATH**
   - Press `Windows + R`, type `sysdm.cpl`, press Enter
   - Click "Advanced" tab → "Environment Variables"
   - Under "System variables", find "Path" → Click "Edit"
   - Click "New" and add: `C:\ffmpeg\bin`
   - Click "OK" on all windows

4. **Verify Installation**
   - Open a **new terminal** (important - restart any open terminals)
   - Run: `ffmpeg -version`
   - You should see version information

## Option 4: Portable Installation (No PATH modification)

If you can't modify system PATH, you can use a portable setup:

1. Extract ffmpeg to: `G:\History vs Hype\tools\ffmpeg\`
2. Run the automated setup script:

```bash
cd "G:\History vs Hype\tools\history-clip-tool"
python setup_ffmpeg_portable.py
```

This will configure the clipping tool to use the portable ffmpeg installation.

## Troubleshooting

### "ffmpeg: command not found" after installation

**Solution:** Restart your terminal. PATH changes only take effect in new terminal sessions.

### Still not working?

1. Verify ffmpeg.exe exists:
   - Check `C:\ffmpeg\bin\ffmpeg.exe` or wherever you extracted it
2. Check PATH manually:
   - Run: `echo $PATH` (Git Bash) or `$env:PATH` (PowerShell)
   - Verify your ffmpeg bin directory is listed
3. Try using the full path:
   ```bash
   /c/ffmpeg/bin/ffmpeg -version
   ```

### Permission denied errors

**Solution:** Run your terminal as Administrator when installing.

## After Installation

Once ffmpeg is installed, test the clipping tool:

```bash
cd "G:\History vs Hype\tools\history-clip-tool"
python run.py
```

The tool should start without errors about missing ffmpeg.
