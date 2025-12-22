# 🎵 DontKillMyVibe

Control your media player (MusicBee, Spotify, etc.) with voice commands and smart hotkeys.

---

## 📋 Table of Contents

- [For Users](#-for-users)
  - [Features](#-features)
  - [Quick Setup](#-quick-setup)
  - [Configuration](#️-configuration)
  - [Usage Guide](#-usage-guide)
- [For Developers](#-for-developers)
  - [System Requirements](#-system-requirements)
  - [Development Environment Setup](#-development-environment-setup)
  - [Building the Application](#-building-the-application)
  - [Project Structure](#-project-structure)
  - [Debugging](#-debugging)

---

## 👤 For Users

### ✨ Features

- **Voice Control** (English):
  - `"Save me"` - Open music player and start playing
  - `"Play"` / `"Stop"` - Play/Pause
  - `"Next song"` - Next track
  - `"Previous song"` - Previous track
  - `"Volume up"` / `"Volume down"` - Increase/Decrease volume

- **Smart Hotkeys**:
  - `Alt + Alt` (double tap quickly) - Play/Pause
  - `Alt + ↑` - Volume up
  - `Alt + ↓` - Volume down
  - `Alt + →` - Next track
  - `Alt + ←` - Previous track

- **Interface**:
  - Runs in system tray
  - Settings GUI and debug log viewer
  - Custom icon support

### 📦 Quick Setup

1. **Download files**:
   - Download `dontkillmyvibe.exe` and `config.json` from the `dist/` folder
   - Place both files in the same directory

2. **Run the application**:
   - Double click `dontkillmyvibe.exe`
   - The app will run hidden in the system tray (bottom right corner of taskbar)

### ⚙️ Configuration

Open `config.json` with Notepad or any text editor:

```json
{
  "app_path": "F:\\MusicBee\\MusicBee.exe",
  "icon_path": "D:\\Code\\Python\\dontkillmyvibe\\chikawa.ico"
}
```

#### Changing your music player:

- **app_path**: Path to your music player's .exe file
  - Example MusicBee: `"F:\\MusicBee\\MusicBee.exe"`
  - Example Spotify: `"C:\\Users\\YourName\\AppData\\Roaming\\Spotify\\Spotify.exe"`
  - Example iTunes: `"C:\\Program Files\\iTunes\\iTunes.exe"`
  - **Note**: Use `\\` (double backslash) instead of `\` in Windows paths

- **icon_path** (optional): Path to custom tray icon (.ico file)
  - If not needed, leave empty: `"icon_path": ""`

#### Finding your application path:

1. Right-click on your music player's Desktop shortcut
2. Select "Properties"
3. Copy the path from the "Target" field
4. Replace all `\` with `\\` and paste into `app_path`

### 🎯 Usage Guide

#### First time running:

1. **Allow microphone access**: Windows will prompt for mic permission, click "Allow"
2. **System tray icon**: Look for the icon in the bottom right corner of the taskbar
3. **Right-click the icon** to see the menu:
   - `Show Settings` - Open settings GUI
   - `Quit` - Exit the application

#### Using voice commands:

1. Speak clearly at normal volume
2. Use English commands (listed above)
3. Wait ~1-2 seconds for processing

#### Using hotkeys:

- Hotkeys work immediately without needing the music player in focus
- Press `Alt` twice quickly (< 0.4 seconds) for play/pause

#### Troubleshooting:

- **Voice not recognized**: 
  - Check if microphone is working
  - Verify Windows microphone permissions
  - Settings → Privacy → Microphone → Allow apps to access mic

- **Voice commands not working**:
  - Right-click icon → Show Settings → Enable Debug mode
  - Check logs to see if the app is hearing you

- **Hotkeys not working**:
  - Run the application as Administrator (right-click → Run as admin)

---

## 👨‍💻 For Developers

### 🔧 System Requirements

- **Python**: 3.8 or higher (recommended 3.10+)
- **OS**: Windows 10/11 (application uses Windows-specific features)
- **Microphone**: Any mic (built-in or external)
- **PyAudio dependencies**: Requires Microsoft C++ Build Tools

### 🚀 Development Environment Setup

#### 1. Clone/Download project

```powershell
cd D:\Code\Python
git clone <repository-url> dontkillmyvibe
cd dontkillmyvibe
```

#### 2. Create virtual environment

```powershell
# Create venv
python -m venv .venv

# Activate venv
.venv\Scripts\activate

# Verify Python in venv
python --version
```

#### 3. Install dependencies

```powershell
# Install all packages
pip install -r requirements.txt
```

**PyAudio Note**:

PyAudio requires Microsoft C++ Build Tools. If you encounter errors:

```powershell
# Option 1: Install prebuilt wheel
pip install pipwin
pipwin install pyaudio

# Option 2: Download wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# Choose appropriate file (e.g., PyAudio‑0.2.11‑cp310‑cp310‑win_amd64.whl for Python 3.10, 64-bit)
pip install PyAudio‑0.2.11‑cp310‑cp310‑win_amd64.whl
```

#### 4. Configure config.json

Create or edit `config.json`:

```json
{
  "app_path": "F:\\MusicBee\\MusicBee.exe",
  "icon_path": "D:\\Code\\Python\\dontkillmyvibe\\chikawa.ico"
}
```

#### 5. Run from source

```powershell
# Make sure venv is activated
.venv\Scripts\activate

# Run
python dontkillmyvibe.py
```

### 📦 Building the Application

#### Build exe with PyInstaller:

```powershell
# Activate venv
.venv\Scripts\activate

# Method 1: Use build script (recommended)
build.bat

# Method 2: Manual build
pyinstaller --clean --noconfirm --onefile --noconsole --icon=app.ico --add-data "config.json:." dontkillmyvibe.py
copy config.json dist\
```

**Output**:
- Exe file: `dist/dontkillmyvibe.exe`
- Config: `dist/config.json` (automatically copied)

#### Build options explained:

- `--onefile`: Build as a single exe file
- `--noconsole`: Hide console window, run as GUI app
- `--icon=app.ico`: Icon for the exe (if app.ico exists)
- `--add-data "config.json:."`: Include config.json in exe
- `--clean`: Remove old build cache

#### Customizing build:

Edit `dontkillmyvibe.spec` to change build settings:

```python
# Example: add hidden imports
hiddenimports=['pystray._win32']

# Example: add data files
datas=[('config.json', '.'), ('icons/', 'icons/')]
```

Then build using spec file:

```powershell
pyinstaller dontkillmyvibe.spec
```

### 📁 Project Structure

```
dontkillmyvibe/
├── dontkillmyvibe.py       # Main source code
├── config.json             # User config file
├── requirements.txt        # Python dependencies
├── build.bat              # Build script
├── dontkillmyvibe.spec    # PyInstaller spec
├── app.ico                # Icon file (optional)
├── chikawa.ico           # Tray icon
├── .venv/                # Virtual environment (created)
├── build/                # Build temp files (generated)
├── dist/                 # Output exe and files (generated)
└── debug.log            # Log file (generated when debug mode ON)
```

### 🐛 Debugging

#### Enable debug mode:

1. **In code**:
```python
# Edit in dontkillmyvibe.py
DEBUG = True  # Instead of False
```

2. **Via GUI**:
   - Right-click icon → Show Settings
   - Check "Debug Mode"
   - Click "Open Console" to view live log

#### Log file:

- **Location**: `debug.log` (same directory as exe/script)
- **Encoding**: UTF-8
- **Format**: `timestamp - level - message`

#### View log in realtime:

```powershell
# PowerShell
Get-Content debug.log -Wait -Tail 50

# Or use built-in function
# When debug mode is ON, automatically opens PowerShell window with tail log
```

#### Common debug scenarios:

**Test voice recognition**:
```python
# In process_audio(), check logs:
# "🔄 Processing audio..." - Processing
# "📝 Detected: play music" - Received text
# "✅ Executing: play" - Executing command
```

**Test keyboard hooks**:
```python
# In on_key_press(), log each key press
log(f"Key pressed: {key}")
```

**Test API calls**:
```python
# Google Speech Recognition errors
# "❌ API error: ..." - API connection error
# "❌ Could not understand audio" - Audio not understood
```

### 🔨 Development Workflow

1. **Edit code**: Modify `dontkillmyvibe.py`
2. **Test**: 
   ```powershell
   .venv\Scripts\activate
   python dontkillmyvibe.py
   ```
3. **Debug**: Enable DEBUG mode, check logs
4. **Build**: Run `build.bat`
5. **Test exe**: Run `dist/dontkillmyvibe.exe`

### 📚 Dependencies Details

| Package | Version | Purpose |
|---------|---------|---------|
| SpeechRecognition | Latest | Voice recognition, Google Speech API |
| pynput | Latest | Keyboard/mouse control and listening |
| PyAudio | Latest | Audio input from microphone |
| pystray | Latest | System tray icon |
| Pillow | Latest | Image processing for icons |

### 🎓 Code Structure Overview

```python
# Main components:

VoiceController              # Main class
├── __init__()              # Initialize recognizer, keyboard controller
├── commands{}              # Dict mapping voice commands → actions
├── run()                   # Main loop, background listening
├── process_audio()         # Callback for processing voice input
├── on_key_press()          # Keyboard hotkey handler
└── Action methods:
    ├── open_and_play()     # Open app and play
    ├── play_pause()        # Toggle play/pause
    ├── next_media()        # Next track
    ├── previous_media()    # Previous track
    ├── volume_up()         # Increase volume
    └── volume_down()       # Decrease volume

GUI components:
├── show_settings_gui()     # Settings window
├── SystemTrayIcon          # Tray icon with menu
└── log_widget             # Debug log display

Helper functions:
├── load_config()          # Load config.json
├── log()                  # Logging function
└── ensure_console()       # Open PowerShell debug console
```

### 💡 Development Tips

1. **Virtual environment**: Always use venv to avoid dependency conflicts
2. **PyAudio installation**: If difficulties arise, use prebuilt wheel
3. **Build testing**: Test both debug and release builds
4. **Icon formats**: Icon must be .ico format, not .png
5. **Path separators**: In config.json, use `\\` or `/`, never single `\`
6. **Google API**: Voice recognition requires internet, uses Google Speech API free tier
7. **Admin rights**: Some keyboard hooks need admin privileges to work with elevated apps

### 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m 'Add some AmazingFeature'`
4. Push to branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

### 📝 License

[Add your license here]

### 📧 Contact

[Add your contact information here]

---

**Enjoy your music without interruption! 🎵✨**
