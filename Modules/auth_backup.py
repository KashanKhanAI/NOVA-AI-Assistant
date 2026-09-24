import hashlib
import getpass
import os

PASSWORD_FILE = "owner.key"


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def setup_owner():
    if os.path.exists(PASSWORD_FILE):
        return

    print("=== OWNER SETUP ===")

    while True:
        password = getpass.getpass("Create owner password: ")
        confirm = getpass.getpass("Confirm password: ")

        if len(password) < 8:
            print("Password must be at least 8 characters.")
            continue

        if password != confirm:
            print("Passwords do not match.")
            continue

        with open(PASSWORD_FILE, "w", encoding="utf-8") as file:
            file.write(hash_password(password))

        print("Owner authentication created.")
        break


def authenticate():
    if not os.path.exists(PASSWORD_FILE):
        setup_owner()

    for attempt in range(3):
        password = getpass.getpass("Owner password: ")

        with open(PASSWORD_FILE, "r", encoding="utf-8") as file:
            saved_hash = file.read().strip()

        if hash_password(password) == saved_hash:
            print("Owner verified.")
            return True

        print("Incorrect password.")

    print("ACCESS LOCKED.")
    return False


if __name__ == "__main__":
    print("Owner Authentication System")
    
    if authenticate():
        print("Access granted.")
    else:
        print("Access denied.")
