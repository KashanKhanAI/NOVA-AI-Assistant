from .device_lock import verify_device
from .auth import authenticate
from .permissions import show_permissions, set_permission


def admin_settings():
    print("\n==============================")
    print("       SECURE OWNER SETTINGS")
    print("==============================")

    if not verify_device():
        print("DEVICE NOT AUTHORIZED.")
        return

    if not authenticate():
        print("ACCESS DENIED.")
        return

    print("Owner verified.")
    print("Authorized device verified.")

    while True:
        print("\n------------------------------")
        print("1. Security status")
        print("2. Camera permission")
        print("3. Microphone permission")
        print("4. File access")
        print("5. Mobile access")
        print("6. Exit")

        choice = input("\nChoose option: ").strip()

        if choice == "1":
            show_permissions()

        elif choice == "2":
            set_permission("camera", True)

        elif choice == "3":
            set_permission("microphone", True)

        elif choice == "4":
            set_permission("files", True)

        elif choice == "5":
            set_permission("mobile", True)

        elif choice == "6":
            print("Owner settings closed.")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    admin_settings()
