from pathlib import Path
import json

LICENSE_FILE = Path(__file__).resolve().parent.parent / "license.json"


def get_license():
    """Return the current NOVA license information."""
    if not LICENSE_FILE.exists():
        return {
            "plan": "free",
            "activated": False
        }

    try:
        with LICENSE_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return {
            "plan": data.get("plan", "free"),
            "activated": bool(data.get("activated", False))
        }

    except (OSError, json.JSONDecodeError):
        return {
            "plan": "free",
            "activated": False
        }


def is_pro():
    """Return True only when NOVA Pro is activated."""
    license_data = get_license()
    return (
        license_data.get("plan") == "pro"
        and license_data.get("activated") is True
    )


def current_plan():
    """Return 'free' or 'pro'."""
    return "pro" if is_pro() else "free"