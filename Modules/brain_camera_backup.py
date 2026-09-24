from .memory import remember, recall
from .security import security_check
def process_command(command):
    command = command.strip()

    if not command:
        return

    if command.lower().startswith("remember "):
        data = command[9:].strip()

        if "=" in data:
            key, value = data.split("=", 1)
            remember(key.strip(), value.strip())
        else:
            print("Use: remember name=value")

        return

    if command.lower().startswith("recall "):
        key = command[7:].strip()
        recall(key)
        return

    if security_check(command):
        print("Command approved.")
    else:
        print("Command blocked.")

