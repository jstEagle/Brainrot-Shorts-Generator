"""
Build script: compiles main.py into an exe and adds it to the Windows startup folder.
Usage: python compile.py
"""

import subprocess
import sys
import os
import platform


def build_exe():
    """Run PyInstaller using main.spec."""
    print("Building executable with PyInstaller...")
    result = subprocess.run(
        [sys.executable, "-m", "PyInstaller", "main.spec", "--noconfirm"],
        cwd=os.path.dirname(os.path.abspath(__file__)),
    )
    if result.returncode != 0:
        print("PyInstaller build failed.")
        sys.exit(1)
    print("Build complete.")


def add_to_startup_windows():
    """Create a shortcut to dist/main.exe in the Windows Startup folder."""
    try:
        import winshell
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "winshell", "pywin32"])
        import winshell

    from win32com.client import Dispatch

    project_dir = os.path.dirname(os.path.abspath(__file__))
    exe_path = os.path.join(project_dir, "dist", "main.exe")

    if not os.path.exists(exe_path):
        print(f"ERROR: {exe_path} not found. Build may have failed.")
        sys.exit(1)

    startup_folder = winshell.startup()
    shortcut_path = os.path.join(startup_folder, "BrainrotGenerator.lnk")

    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = exe_path
    shortcut.WorkingDirectory = project_dir
    shortcut.Description = "Brainrot Shorts Generator"
    shortcut.save()

    print(f"Startup shortcut created: {shortcut_path}")


def add_to_startup_mac():
    """Create a LaunchAgent plist so main runs on login."""
    project_dir = os.path.dirname(os.path.abspath(__file__))
    exe_path = os.path.join(project_dir, "dist", "main")

    if not os.path.exists(exe_path):
        print(f"ERROR: {exe_path} not found. Build may have failed.")
        sys.exit(1)

    plist_dir = os.path.expanduser("~/Library/LaunchAgents")
    os.makedirs(plist_dir, exist_ok=True)
    plist_path = os.path.join(plist_dir, "com.brainrot.generator.plist")

    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.brainrot.generator</string>
    <key>ProgramArguments</key>
    <array>
        <string>{exe_path}</string>
    </array>
    <key>WorkingDirectory</key>
    <string>{project_dir}</string>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
"""
    with open(plist_path, "w") as f:
        f.write(plist_content)

    print(f"LaunchAgent created: {plist_path}")
    print("It will run on next login. To load now: launchctl load " + plist_path)


if __name__ == "__main__":
    build_exe()

    system = platform.system()
    if system == "Windows":
        add_to_startup_windows()
    elif system == "Darwin":
        add_to_startup_mac()
    else:
        print(f"Startup shortcut not supported on {system}. Executable is at dist/main")

    print("Done.")
