# EchoFlow - AI Voice Assistant

Welcome to **EchoFlow**! This is a simple, powerful voice assistant for Windows. It lets you press a button, speak, and it will automatically type out what you said perfectly into *any* app you are using (like Microsoft Word, Chrome, or Discord) using cutting-edge AI.

If you don't know much about computers, don't worry! Follow these step-by-step instructions.

---

## Part 1: Setting it up for the first time

To run this app, you just need a few basic things installed on your computer.

### Step 1: Install Python and Git
1. **Download Python:** Go to [python.org/downloads](https://www.python.org/downloads/) and click "Download Python 3.11" (or whatever the latest version is). 
   - **VERY IMPORTANT:** When you open the installer, check the box at the very bottom that says **"Add python.exe to PATH"** before you click Install.
2. **Download Git:** Go to [git-scm.com/downloads](https://git-scm.com/downloads) and download/install Git for Windows. You can just click "Next" on all the default settings.

### Step 2: Download the Code
1. Click your Windows Start button, type `cmd`, and open **Command Prompt**.
2. Type this exact command and press Enter to download the app to your computer:
   ```cmd
   git clone https://github.com/your-username/echoflow.git
   ```
3. Type this to go inside the newly downloaded folder:
   ```cmd
   cd echoflow
   ```

### Step 3: Install the App
While still in the Command Prompt (inside the `echoflow` folder), copy and paste these commands one by one, pressing Enter after each:

1. Create a safe "virtual" space for the app:
   ```cmd
   python -m venv venv
   ```
2. Turn on the virtual space:
   ```cmd
   venv\Scripts\activate
   ```
3. Install all the necessary robot brains:
   ```cmd
   pip install -e .
   ```

### Step 4: Get your free NVIDIA AI Key
EchoFlow uses NVIDIA's supercomputers to make your text perfect.
1. Go to [build.nvidia.com](https://build.nvidia.com) and sign up for a free account.
2. Look for "API Keys" in your account settings and generate a new key. It will look like a long string of random letters and numbers.
3. Open the `echoflow` folder on your computer. 
4. Find the file named `.env.example`, right-click it, and rename it to just `.env` (make sure there is a dot at the beginning).
5. Open that `.env` file in Notepad. Delete the placeholder text and paste your key so it looks like this:
   ```ini
   NVIDIA_API_KEY=your_long_api_key_goes_here
   
   # Optional: Change the hotkey (default is ctrl+space)
   ECHOFLOW_HOTKEY=ctrl+alt+space
   ```
6. Save and close Notepad.

### Step 5: Start the App!
In your Command Prompt, type:
```cmd
python app/main.py
```
Look at the bottom right of your screen (near the clock). You should see a new microphone icon! **You are ready.** 
Click anywhere you want to type, press `Ctrl + Alt + Space` on your keyboard, and start talking!

---

## Part 2: How to make it run automatically on Startup

You probably don't want to open Command Prompt every time you restart your computer. Let's make Windows open it automatically!

1. Open your `echoflow` folder. Right-click anywhere in the empty space, select **New**, and then click **Text Document**.
2. Name it `start_echoflow.bat` (make sure you delete the `.txt` part at the end. Windows might warn you about changing the extension, click Yes).
3. Right-click `start_echoflow.bat` and click **Edit** (this will open Notepad).
4. Paste the following text into Notepad exactly as it is:
   ```bat
   @echo off
   cd /d "%~dp0"
   call venv\Scripts\activate.bat
   start /B pythonw app/main.py
   ```
5. Save and close Notepad. *(If you double-click this file now, it will secretly start the app in the background!)*
6. Now, hold the `Windows Key` on your keyboard and press `R`. A small "Run" box will appear.
7. Type `shell:startup` into the box and press Enter. A folder will pop open.
8. Right-click your new `start_echoflow.bat` file, and click **Create shortcut**.
9. Drag that shortcut into the `Startup` folder that popped open in Step 7.

**You're done!** Now, every time you turn on your PC, EchoFlow will wake up in the background and wait for your hotkey. 

---

### Need to check logs or change modes?
Just right-click the microphone icon near your clock. You can switch between Formal or Casual typing, and even open the logs if something breaks. Enjoy!
