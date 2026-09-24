import hashlib
import getpass
from pathlib import Path

# NOVA/PrivateVault/owner.key
BASE_DIR = Path(__file__).resolve().parent.parent
PASSWORD_FILE = BASE_DIR / "PrivateVault" / "owner.key"


def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def setup_owner():
    if PASSWORD_FILE.exists():
        return

    PASSWORD_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    print("=== NOVA OWNER SETUP ===")

    while True:
        password = getpass.getpass(
            "Create owner password: "
        )

        confirm = getpass.getpass(
            "Confirm password: "
        )

        if len(password) < 8:
            print(
                "Password must be at least 8 characters."
            )
            continue

        if password != confirm:
            print("Passwords do not match.")
            continue

        PASSWORD_FILE.write_text(
            hash_password(password),
            encoding="utf-8"
        )

        print("Owner authentication created.")
        break


def authenticate():
    if not PASSWORD_FILE.exists():
        setup_owner()

    for attempt in range(3):
        password = getpass.getpass(
            "NOVA Owner password: "
        )

        saved_hash = PASSWORD_FILE.read_text(
            encoding="utf-8"
        ).strip()

        if hash_password(password) == saved_hash:
            print("Owner verified.")
            return True

        remaining = 2 - attempt

        if remaining > 0:
            print(
                f"Incorrect password. "
                f"Attempts remaining: {remaining}"
            )

    print("ACCESS LOCKED.")
    return False


if __name__ == "__main__":
    print("NOVA Owner Authentication System")

    if authenticate():
        print("Access granted.")
    else:
        print("Access denied.")
