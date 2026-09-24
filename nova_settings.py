import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
CONFIG_DIR = BASE_DIR / "Config"
SETTINGS_FILE = CONFIG_DIR / "nova_settings.json"


DEFAULT_SETTINGS = {
    "assistant_name": "NOVA",
    "ai_engine": "OpenJarvis + Ollama",
    "voice_enabled": True,
    "memory_enabled": True,
    "security_enabled": True
}


def load_settings():
    CONFIG_DIR.mkdir(exist_ok=True)

    if not SETTINGS_FILE.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            settings = json.load(file)

        result = DEFAULT_SETTINGS.copy()
        result.update(settings)
        return result

    except Exception:
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    CONFIG_DIR.mkdir(exist_ok=True)

    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(
            settings,
            file,
            indent=4,
            ensure_ascii=False
        )


def update_setting(key, value):
    settings = load_settings()
    settings[key] = value
    save_settings(settings)


if __name__ == "__main__":
    print(load_settings())