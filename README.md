# EchoFlow - AI Voice Assistant

EchoFlow is a powerful, production-ready AI voice-to-text and voice-assistant application designed for Windows. It allows you to press a global hotkey, speak naturally, and instantly have your words transcribed, formatted by AI, and inserted into whatever application you are currently using.

## Features
- **Global Hotkey Integration**: Press `Ctrl+Alt+Space` from anywhere to start recording.
- **NVIDIA AI Powered**: Uses lightning-fast NVIDIA NIM APIs for Speech-to-Text and LLM transformation.
- **AI Formatting Modes**: Choose between Default, Formal, Casual, and Code modes via the System Tray.
- **App-Aware Context**: Automatically detects the active window (e.g., VS Code, Word) to provide domain-specific formatting.
- **Voice Commands**: Speak commands like "press enter" or "undo" to trigger keyboard shortcuts.
- **Snippets & Dictionary**: Automatically expand phrases like "insert signature" or correct jargon before it reaches the AI.
- **Local History**: A lightweight local SQLite database saves your dictation history.

---

## Getting Started (Development Setup)

### 1. Prerequisites
- **Python 3.11** or higher
- **Git**
- An **NVIDIA API Key** (Get one from [build.nvidia.com](https://build.nvidia.com))

### 2. Clone the Repository
```cmd
git clone https://github.com/your-username/echoflow.git
cd echoflow
```

### 3. Create a Virtual Environment & Install
Create a Python virtual environment to keep dependencies isolated:
```cmd
python -m venv venv
venv\Scripts\activate
```

Install the application and its dependencies:
```cmd
pip install -e .
```
*(If you want to run tests or build the `.exe`, install the developer tools with `pip install -e .[dev]`)*

### 4. Configuration
Create a file named `.env` in the root directory of the project and add your NVIDIA API Key:
```ini
NVIDIA_API_KEY=your_api_key_here
```

### 5. Run the Application
Start the app directly from source:
```cmd
python app/main.py
```
You should see the EchoFlow icon appear in your Windows System Tray (bottom right corner).

---

## Building a Standalone Executable
If you want to package EchoFlow into a `.exe` so you don't need to use the command line:

1. Ensure dev tools are installed: `pip install -e .[dev]`
2. Run the build script:
```cmd
python build.py
```
3. The executable will be generated inside the `dist/EchoFlow/` folder. You can run `EchoFlow.exe` directly.

### Creating a Windows Installer
To create an official installer (`Setup.exe`):
1. Download and install [Inno Setup](https://jrsoftware.org/isinfo.php).
2. Right-click the `echoflow.iss` file in the project folder and select **Compile**.
3. The installer will be placed in the `Output` folder.

---

## How to Make EchoFlow a Startup App

If you want EchoFlow to start automatically whenever you turn on your PC:

**Method 1: Windows Startup Folder (Easiest)**
1. Press `Win + R` on your keyboard to open the Run dialog.
2. Type `shell:startup` and press Enter. This opens your Windows Startup folder.
3. Find your built `EchoFlow.exe` (inside the `dist/EchoFlow` folder).
4. Right-click `EchoFlow.exe` and select **Create shortcut**.
5. Drag and drop that new shortcut into the `Startup` folder you opened in Step 2.

**Method 2: Using the Inno Setup Installer**
If you build the project using the provided `echoflow.iss` script, you can easily modify the script to add a registry key that runs the app on startup. Add this under the `[Registry]` section of the `.iss` file:
```ini
[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "EchoFlow"; ValueData: """{app}\EchoFlow.exe"""; Flags: uninsdeletevalue
```
When you run the installer, it will automatically configure Windows to launch EchoFlow on boot.
