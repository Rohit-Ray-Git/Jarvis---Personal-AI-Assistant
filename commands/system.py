# system.py
# Placeholder for system control commands (open apps, shutdown, etc.) 

import os
import subprocess
import webbrowser
import shutil

def open_chrome():
    try:
        path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        subprocess.Popen([path])
        return "Opening Chrome."
    except Exception as e:
        return f"Failed to open Chrome: {e}"

def shutdown():
    try:
        os.system("shutdown /s /t 1")
        return "Shutting down the system."
    except Exception as e:
        return f"Failed to shutdown: {e}"

def open_folder(folder_name):
    try:
        user_folder = os.path.expanduser("~")
        folder_path = os.path.join(user_folder, folder_name)
        if os.path.exists(folder_path):
            os.startfile(folder_path)
            return f"Opening folder {folder_name}."
        else:
            return f"Folder '{folder_name}' not found."
    except Exception as e:
        return f"Failed to open folder: {e}"

def open_default_browser(url=None):
    try:
        if url:
            webbrowser.open(url)
            return f"Opening {url} in your default browser."
        else:
            webbrowser.open('https://www.google.com')
            return "Opening your default browser."
    except Exception as e:
        return f"Failed to open browser: {e}"

def open_application(app_name):
    try:
        # Try to open by name (works for apps in PATH)
        try:
            subprocess.Popen([app_name])
            return f"Opening {app_name}."
        except Exception:
            pass
        # Try common Windows locations
        possible_paths = [
            os.path.join(os.environ.get('ProgramFiles', ''), app_name + '.exe'),
            os.path.join(os.environ.get('ProgramFiles(x86)', ''), app_name + '.exe'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), app_name + '.exe'),
            shutil.which(app_name)
        ]
        for path in possible_paths:
            if path and os.path.exists(path):
                os.startfile(path)
                return f"Opening {app_name}."
        return f"Could not find application '{app_name}'."
    except Exception as e:
        return f"Failed to open application: {e}" 