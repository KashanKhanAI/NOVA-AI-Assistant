import json
import re

from Modules.ai_brain import ask_ai


SYSTEM_PROMPT = """
You are NOVA's action planner.

Return ONLY valid JSON.

Allowed actions:
- OPEN_APP
- OPEN_FOLDER
- OPEN_WEBSITE
- ANSWER

Rules:

1. Use OPEN_APP only when the user clearly asks to open,
   launch, start, run, or kholo an application.

2. Use OPEN_FOLDER only when the user clearly asks to open
   a folder/directory.

3. Use OPEN_WEBSITE only when the user clearly asks to open
   a website.

4. Questions, explanations, planning, creating, designing,
   discussing, or showing something MUST be ANSWER.

5. Never invent an application name.

6. If the command is unclear, use ANSWER.

7. Preserve the user's intended target.

Examples:

User: WhatsApp kholo
{"action":"OPEN_APP","target":"WhatsApp"}

User: Chrome khol do
{"action":"OPEN_APP","target":"Chrome"}

User: Notepad start karo
{"action":"OPEN_APP","target":"Notepad"}

User: Downloads kholo
{"action":"OPEN_FOLDER","target":"Downloads"}

User: YouTube kholo
{"action":"OPEN_WEBSITE","target":"https://www.youtube.com"}

User: Pakistan ka capital kya hai
{"action":"ANSWER","target":""}

User: NOVA ka structure banao
{"action":"ANSWER","target":""}

Return ONLY valid JSON.
"""


OPEN_WORDS = (
    "open",
    "kholo",
    "khol",
    "kholna",
    "launch",
    "start",
    "run",
    "chalao",
    "chala",
)


ANSWER_WORDS = (
    "banao",
    "bana",
    "bnado",
    "bna do",
    "bna kar do",
    "structure",
    "sturcher",
    "architecture",
    "design",
    "dikhao",
    "dikhana",
    "samjhao",
    "explain",
    "help",
    "plan",
    "kaise",
    "kya hai",
    "batao",
    "what is",
)


KNOWN_APPS = {
    "whatsapp": "WhatsApp",
    "chrome": "Chrome",
    "notepad": "Notepad",
    "calculator": "Calculator",
    "calc": "Calculator",
    "paint": "Paint",
    "edge": "Edge",
    "explorer": "Explorer",
}


KNOWN_FOLDERS = {
    "downloads": "Downloads",
    "documents": "Documents",
    "desktop": "Desktop",
    "pictures": "Pictures",
    "videos": "Videos",
    "music": "Music",
}


def _contains_any(text, words):
    return any(word in text for word in words)


def _safe_rule(command):
    text = command.lower().strip()

    text = re.sub(
        r"^\s*nova[\s,:-]*",
        "",
        text
    ).strip()

    # Never turn explanation/creation commands into actions.
    if _contains_any(text, ANSWER_WORDS):
        return {
            "action": "ANSWER",
            "target": ""
        }

    if not _contains_any(text, OPEN_WORDS):
        return None

    # Website
    if "youtube" in text:
        return {
            "action": "OPEN_WEBSITE",
            "target": "https://www.youtube.com"
        }

    # Known applications
    for name, target in KNOWN_APPS.items():
        if name in text:
            return {
                "action": "OPEN_APP",
                "target": target
            }

    # Known folders
    for name, target in KNOWN_FOLDERS.items():
        if name in text:
            return {
                "action": "OPEN_FOLDER",
                "target": target
            }

    return None


def _validate_action(result):
    if not isinstance(result, dict):
        return {
            "action": "ANSWER",
            "target": ""
        }

    allowed_actions = {
        "OPEN_APP",
        "OPEN_FOLDER",
        "OPEN_WEBSITE",
        "ANSWER",
    }

    action = str(
        result.get("action", "ANSWER")
    ).upper().strip()

    target = str(
        result.get("target", "")
    ).strip()

    if action not in allowed_actions:
        return {
            "action": "ANSWER",
            "target": ""
        }

    if action != "ANSWER" and not target:
        return {
            "action": "ANSWER",
            "target": ""
        }

    return {
        "action": action,
        "target": target
    }


def plan_command(command):
    command = command.strip()

    if not command:
        return {
            "action": "ANSWER",
            "target": ""
        }

    safe_action = _safe_rule(command)

    if safe_action is not None:
        return safe_action

    prompt = (
        SYSTEM_PROMPT
        + "\nUser command:\n"
        + command
    )

    try:
        response = ask_ai(prompt).strip()

        match = re.search(
            r"\{.*\}",
            response,
            re.DOTALL
        )

        if not match:
            return {
                "action": "ANSWER",
                "target": ""
            }

        result = json.loads(match.group())

        return _validate_action(result)

    except Exception:
        # AI failure must never trigger a computer action.
        return {
            "action": "ANSWER",
            "target": ""
        }