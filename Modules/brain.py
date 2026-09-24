from .memory import remember, recall
from .security import security_check
from .camera import start_camera


def process_command(command):
    if not command:
        return

    command = command.strip()
    lower_command = command.lower()

    # Remember
    if lower_command.startswith("remember "):
        data = command[9:].strip()

        if "=" in data:
            key, value = data.split("=", 1)
            remember(key.strip(), value.strip())
        else:
            print("Use: remember name=value")

        return

    # Recall
    if lower_command.startswith("recall "):
        key = command[7:].strip()
        recall(key)
        return

    # Camera
    camera_commands = [
        "camera on",
        "camera on karo",
        "camera kholo",
        "camera khol do",
        "camera start",
        "camera start karo",
    ]

    if any(item in lower_command for item in camera_commands):
        print("NOVA: Camera permission check kar rahi hoon.")

        if start_camera():
            print("NOVA: Camera successfully started.")
        else:
            print("NOVA: Camera start nahi ho saka.")

        return

    # Security
    if security_check(command):
        print("Command approved.")
    else:
        print("Command blocked.")
