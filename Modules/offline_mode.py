import socket
from datetime import datetime
import subprocess
import os


def internet_available(timeout=2):
    try:
        socket.create_connection(("1.1.1.1", 53), timeout=timeout)
        return True
    except OSError:
        return False


def connection_status():
    return "ONLINE" if internet_available() else "OFFLINE"


def local_time():
    return datetime.now().strftime("%I:%M:%S %p")


def run_local_command(command):
    command = command.strip().lower()

    if command in ("time", "what time is it"):
        return f"Current time: {local_time()}"

    if command == "internet status":
        return f"Internet: {connection_status()}"

    if command == "offline status":
        return "Offline mode is available. Local functions can continue."

    if command == "open calculator":
        subprocess.Popen("calc.exe")
        return "Calculator opened."

    if command == "open notepad":
        subprocess.Popen("notepad.exe")
        return "Notepad opened."

    if command == "open folder":
        os.startfile(os.getcwd())
        return "Project folder opened."

    return "This command is not available offline."


if __name__ == "__main__":
    print("=== JARVIS OFFLINE MODE TEST ===")
    print(f"Internet: {connection_status()}")
    print(run_local_command("time"))
    print(run_local_command("offline status"))
