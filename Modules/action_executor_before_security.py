import os
import subprocess
import webbrowser
from pathlib import Path

from Modules.app_discovery import open_discovered_app


def open_folder(folder_name):
    name = folder_name.lower().strip()

    folders = {
        "downloads": Path.home() / "Downloads",
        "documents": Path.home() / "Documents",
        "desktop": Path.home() / "Desktop",
        "pictures": Path.home() / "Pictures",
        "videos": Path.home() / "Videos",
        "music": Path.home() / "Music",
    }

    folder = folders.get(name)

    if folder and folder.exists():
        os.startfile(str(folder))
        return f"Opened {name}."

    return f"I couldn't find the folder '{folder_name}'."


def open_settings():
    try:
        subprocess.Popen("start ms-settings:", shell=True)
        return "Opened Windows Settings."
    except Exception as error:
        return f"Could not open Settings: {error}"


def execute_action(action):
    action_type = action.get("action", "ANSWER")
    target = action.get("target", "")

    if action_type == "OPEN_APP":
        return open_discovered_app(target)

    if action_type == "OPEN_FOLDER":
        return open_folder(target)

    if action_type == "OPEN_WEBSITE":
        webbrowser.open(target)
        return f"Opened {target}."

    if action_type == "OPEN_SETTINGS":
        return open_settings()

    if action_type == "ANSWER":
        return target

    return f"I don't know how to execute '{action_type}'."
