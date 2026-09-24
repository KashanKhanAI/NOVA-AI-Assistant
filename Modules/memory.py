import json
import os
from pathlib import Path


# Always use the NOVA project folder for memory.json
BASE_DIR = Path(__file__).resolve().parent.parent
MEMORY_FILE = BASE_DIR / "memory.json"


def load_memory():
    """Load NOVA memory safely."""
    if not MEMORY_FILE.exists():
        return {}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict):
            return data

        return {}

    except (json.JSONDecodeError, OSError):
        return {}


def save_memory(memory):
    """Save NOVA memory safely."""
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as file:
            json.dump(
                memory,
                file,
                indent=4,
                ensure_ascii=False
            )

        return True

    except OSError:
        return False


def remember(key, value):
    """Remember a key/value pair."""
    key = str(key).strip().lower()
    value = str(value).strip()

    if not key:
        return False, "Memory key cannot be empty."

    if not value:
        return False, "Memory value cannot be empty."

    memory = load_memory()
    memory[key] = value

    if save_memory(memory):
        print("Memory saved.")
        return True, f"I will remember {key}."

    return False, "I couldn't save that memory."


def recall(key):
    """Recall a saved value."""
    key = str(key).strip().lower()

    if not key:
        return None

    memory = load_memory()

    if key in memory:
        print("Memory:", memory[key])
        return memory[key]

    print("No memory found.")
    return None


if __name__ == "__main__":
    print("NOVA Memory System Test")

    success, message = remember("assistant_name", "NOVA")
    print(message)

    value = recall("assistant_name")
    print("Recalled:", value)