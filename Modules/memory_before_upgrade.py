import json
import os

MEMORY_FILE = "memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}


def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=4, ensure_ascii=False)


def remember(key, value):
    memory = load_memory()
    memory[key] = value
    save_memory(memory)
    print("Memory saved.")


def recall(key):
    memory = load_memory()

    if key in memory:
        print("Memory:", memory[key])
        return memory[key]

    print("No memory found.")
    return None


if __name__ == "__main__":
    print("Memory system is running.")

    remember("assistant_name", "My AI Assistant")
    recall("assistant_name")
