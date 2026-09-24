import os
import subprocess
from pathlib import Path


SPECIAL_APPS = {
    "settings": "ms-settings:",
}


WINDOWS_APPS = {
    "whatsapp": "5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App",
}


def open_app(app_name):
    name = app_name.lower().strip()

    if name in SPECIAL_APPS:
        os.startfile(SPECIAL_APPS[name])
        return f"Opened {name}."

    if name in WINDOWS_APPS:
        app_id = WINDOWS_APPS[name]
        subprocess.Popen(
            [
                "explorer.exe",
                f"shell:AppsFolder\\{app_id}"
            ]
        )
        return f"Opened {name}."

    locations = [
        Path(os.environ.get("PROGRAMDATA", "")) /
        "Microsoft/Windows/Start Menu/Programs",

        Path(os.environ.get("APPDATA", "")) /
        "Microsoft/Windows/Start Menu/Programs",
    ]

    for folder in locations:
        if folder.exists():
            for item in folder.rglob("*"):
                if item.is_file():
                    item_name = item.stem.lower()

                    if name in item_name or item_name in name:
                        try:
                            os.startfile(str(item))
                            return f"Opened {item.stem}."
                        except Exception:
                            pass

    try:
        subprocess.Popen(name)
        return f"Opened {name}."
    except Exception:
        return f"I couldn't find an installed app named '{app_name}'."
