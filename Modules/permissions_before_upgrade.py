import json
import os

PERMISSION_FILE = "permissions.json"

DEFAULT_PERMISSIONS = {
    "camera": False,
    "microphone": False,
    "files": False,
    "mobile": False,
    "computer_control": True
}


def load_permissions():
    if not os.path.exists(PERMISSION_FILE):
        save_permissions(DEFAULT_PERMISSIONS.copy())
        return DEFAULT_PERMISSIONS.copy()

    try:
        with open(PERMISSION_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return DEFAULT_PERMISSIONS.copy()


def save_permissions(permissions):
    with open(PERMISSION_FILE, "w", encoding="utf-8") as file:
        json.dump(permissions, file, indent=4)


def check_permission(name):
    permissions = load_permissions()
    return permissions.get(name, False)


def set_permission(name, value):
    permissions = load_permissions()

    if name not in permissions:
        print("Unknown permission.")
        return

    permissions[name] = value
    save_permissions(permissions)

    status = "ON" if value else "OFF"
    print(f"{name}: {status}")


def show_permissions():
    permissions = load_permissions()

    print("\n=== PERMISSIONS ===")

    for name, value in permissions.items():
        status = "ON" if value else "OFF"
        print(f"{name}: {status}")


if __name__ == "__main__":
    print("Permission Manager")

    show_permissions()
