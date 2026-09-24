from Modules.action_planner import plan_command
from Modules.action_executor import execute_action
from Modules.ai_brain import ask_ai
from Modules.voice import listen
from Modules.memory import remember, recall
from Modules.auth import authenticate


def nova_process(command):
    command = command.strip()

    if not command:
        return ""

    # Memory commands
    lower_command = command.lower()

    if lower_command.startswith("remember "):
        data = command[9:].strip()

        if " as " in data.lower():
            key, value = data.split(" as ", 1)
            key = key.strip()
            value = value.strip()

            if key and value:
                remember(key, value)
                return f"I will remember {key}."

        return "Use: remember key as value"

    if lower_command.startswith("recall "):
        key = command[7:].strip()

        if key:
            value = recall(key)

            if value is not None:
                return f"{key}: {value}"

            return f"I don't have anything saved for {key}."

        return "Use: recall key"
    # Natural memory questions
    if any(phrase in lower_command for phrase in [
        "mera name kia ha",
        "mera naam kia ha",
        "mera name kya ha",
        "mera naam kya ha",
        "what is my name",
        "what''s my name",
        "my name"
    ]):
        value = recall("name")

        if value is not None:
            return f"Mera naam {value} hai."

        return "Mujhe abhi tumhara naam yaad nahi."

    action = plan_command(command)

    print("NOVA PLAN:", action)

    # Computer action
    if action.get("action") != "ANSWER":

        print("NOVA: Owner verification required.")

        if not authenticate():
            return "Action blocked: owner verification failed."

        return execute_action(action)

    # AI answer
    target = action.get("target", "").strip()

    if target:
        return target

    return ask_ai(
        "You are NOVA, a helpful computer assistant. "
        "Answer the user's question clearly and briefly. "
        "User question: " + command
    )


def main():
    print("NOVA is online.")
    print("Press Enter to use voice, or type command.")
    print("Type 'exit' to close.")

    while True:
        choice = input(
            "\nPress Enter for voice or type command: "
        ).strip()

        if choice.lower() == "exit":
            print("NOVA: Goodbye.")
            break

        if choice:
            command = choice
        else:
            command = listen()

        if not command:
            continue

        print("You:", command)

        try:
            result = nova_process(command)
            print("NOVA:", result)

        except Exception as error:
            print("NOVA ERROR:", error)


if __name__ == "__main__":
    main()


