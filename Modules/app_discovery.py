import json
import os
import subprocess
from pathlib import Path


def get_start_apps():
    """
    Windows Start Menu se installed applications discover karta hai.
    """

    apps = []

    try:
        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Get-StartApps | Select-Object Name, AppID | ConvertTo-Json"
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            return []

        data = json.loads(result.stdout)

        if isinstance(data, dict):
            data = [data]

        for app in data:
            name = app.get("Name", "").strip()
            app_id = app.get("AppID", "").strip()

            if name and app_id:
                apps.append({
                    "name": name,
                    "app_id": app_id,
                    "type": "start_app"
                })

    except Exception:
        pass

    return apps


def find_exe_apps():
    """
    Common Windows locations mein executable applications dhoondta hai.
    """

    apps = []

    locations = [
        Path(os.environ.get("ProgramFiles", r"C:\Program Files")),
        Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")),
        Path(os.environ.get("LOCALAPPDATA", "")),
    ]

    for location in locations:
        if not location.exists():
            continue

        try:
            for exe in location.rglob("*.exe"):
                apps.append({
                    "name": exe.stem,
                    "path": str(exe),
                    "type": "exe"
                })
        except (PermissionError, OSError):
            continue

    return apps


def find_app(app_name):
    """
    Installed applications mein matching application dhoondta hai.
    """

    query = app_name.lower().strip()

    # Start Menu apps pehle search karo
    apps = get_start_apps()

    # Exact match
    for app in apps:
        if app["name"].lower() == query:
            return app

    # Partial match
    for app in apps:
        if query in app["name"].lower():
            return app

    # EXE applications search karo
    exe_apps = find_exe_apps()

    # Exact match
    for app in exe_apps:
        if app["name"].lower() == query:
            return app

    # Partial match
    for app in exe_apps:
        if query in app["name"].lower():
            return app

    return None


def open_discovered_app(app_name):
    """
    Discovered Windows application ko open karta hai.
    """

    app = find_app(app_name)

    if not app:
        return f"I couldn't find an installed app named '{app_name}'."

    try:

        if app["type"] == "start_app":
            subprocess.Popen(
                [
                    "explorer.exe",
                    f"shell:AppsFolder\\{app['app_id']}"
                ]
            )

        elif app["type"] == "exe":
            subprocess.Popen([app["path"]])

        return f"Opened {app['name']}."

    except Exception as error:
        return f"Could not open {app['name']}: {error}"
