import hashlib
import json
import os
import platform
import uuid

DEVICE_FILE = "device.lock"


def get_device_fingerprint():
    data = {
        "machine": platform.machine(),
        "system": platform.system(),
        "release": platform.release(),
        "processor": platform.processor(),
        "node": platform.node(),
        "mac": uuid.getnode(),
    }

    raw = json.dumps(data, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def register_device():
    fingerprint = get_device_fingerprint()

    with open(DEVICE_FILE, "w", encoding="utf-8") as file:
        file.write(fingerprint)

    print("This computer is now registered.")


def verify_device():
    if not os.path.exists(DEVICE_FILE):
        print("No registered device found.")
        return False

    with open(DEVICE_FILE, "r", encoding="utf-8") as file:
        saved = file.read().strip()

    current = get_device_fingerprint()

    if saved == current:
        print("Authorized device.")
        return True

    print("Unauthorized device.")
    return False


if __name__ == "__main__":
    if not os.path.exists(DEVICE_FILE):
        register_device()

    verify_device()
