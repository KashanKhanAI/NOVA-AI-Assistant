import json
import os
from datetime import datetime


SCOPE_FILE = "security_scope.json"
LOG_FILE = "security_audit.log"


def audit_log(action, result):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = {
        "timestamp": timestamp,
        "action": action,
        "result": result,
    }

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(entry) + "\n")


def create_scope():
    if os.path.exists(SCOPE_FILE):
        return

    scope = {
        "authorized": True,
        "targets": [],
        "notes": "Only test systems explicitly added by the owner."
    }

    with open(SCOPE_FILE, "w", encoding="utf-8") as file:
        json.dump(scope, file, indent=4)


def load_scope():
    create_scope()

    with open(SCOPE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def add_target(target):
    scope = load_scope()

    if target not in scope["targets"]:
        scope["targets"].append(target)

        with open(SCOPE_FILE, "w", encoding="utf-8") as file:
            json.dump(scope, file, indent=4)

        audit_log(
            "TARGET_ADDED",
            f"Authorized target added: {target}"
        )

        print(f"Authorized target added: {target}")
    else:
        print("Target already exists.")


def list_targets():
    scope = load_scope()

    print("\n=== AUTHORIZED SECURITY SCOPE ===")

    if not scope["targets"]:
        print("No authorized targets configured.")
        return

    for number, target in enumerate(scope["targets"], 1):
        print(f"{number}. {target}")


def is_authorized(target):
    scope = load_scope()

    return (
        scope.get("authorized") is True
        and target in scope.get("targets", [])
    )


def security_status():
    scope = load_scope()

    print("\n=== SECURITY MODE ===")
    print(f"Authorized mode: {scope.get('authorized')}")
    print(f"Targets: {len(scope.get('targets', []))}")
    print(f"Audit log: {LOG_FILE}")


if __name__ == "__main__":
    print("=== JARVIS AUTHORIZED SECURITY MODE ===")

    security_status()

    print("\nCommands:")
    print("add <target>")
    print("list")
    print("check <target>")
    print("exit")

    while True:
        command = input("\nSecurity> ").strip()

        if command.lower() == "exit":
            break

        if command.lower() == "list":
            list_targets()
            continue

        if command.lower().startswith("add "):
            target = command[4:].strip()

            if target:
                add_target(target)
            continue

        if command.lower().startswith("check "):
            target = command[6:].strip()

            if is_authorized(target):
                print("AUTHORIZED TARGET")
                audit_log("TARGET_CHECK", f"Allowed: {target}")
            else:
                print("BLOCKED: target is outside authorized scope.")
                audit_log("TARGET_CHECK", f"Blocked: {target}")

            continue

        print("Unknown command.")
