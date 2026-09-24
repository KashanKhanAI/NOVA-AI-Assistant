import os
import subprocess
import webbrowser
from pathlib import Path

from Modules.app_discovery import open_discovered_app
from Modules.permissions import check_permission


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


def open_website(url):
    try:
        webbrowser.open(url)
        return f"Opened {url}."

    except Exception as error:
        return f"Could not open website: {error}"


def execute_action(action):
    """
    Execute only validated NOVA actions.
    """

    if not isinstance(action, dict):
        return "Invalid action."

    action_type = str(
        action.get("action", "ANSWER")
    ).upper().strip()

    target = str(
        action.get("target", "")
    ).strip()

    permission_map = {
        "OPEN_APP": "computer_control",
        "OPEN_FOLDER": "files",
        "OPEN_WEBSITE": "computer_control",
        "OPEN_SETTINGS": "computer_control",
    }

    required_permission = permission_map.get(action_type)

    if required_permission:
        if not check_permission(required_permission):
            return (
                f"Action blocked: "
                f"'{required_permission}' permission is OFF."
            )

    if action_type == "OPEN_APP":
        if not target:
            return "Application name is missing."

        return open_discovered_app(target)

    if action_type == "OPEN_FOLDER":
        if not target:
            return "Folder name is missing."

        return open_folder(target)

    if action_type == "OPEN_WEBSITE":
        if not target:
            return "Website address is missing."

        return open_website(target)

    if action_type == "OPEN_SETTINGS":
        return open_settings()

    if action_type == "ANSWER":
        return target

    return f"I don't know how to execute '{action_type}'." 