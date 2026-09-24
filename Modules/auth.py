import hashlib
import tkinter as tk
from tkinter import simpledialog, messagebox
from pathlib import Path

# NOVA/PrivateVault/owner.key
BASE_DIR = Path(__file__).resolve().parent.parent
PASSWORD_FILE = BASE_DIR / "PrivateVault" / "owner.key"


def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def create_hidden_root():
    root = tk.Tk()
    root.withdraw()
    return root


def setup_owner():
    if PASSWORD_FILE.exists():
        return True

    PASSWORD_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    root = create_hidden_root()

    try:
        messagebox.showinfo(
            "NOVA Owner Setup",
            "Create your NOVA owner password.\n\n"
            "Password must be at least 8 characters.",
            parent=root
        )

        while True:
            password = simpledialog.askstring(
                "NOVA Owner Setup",
                "Create owner password:",
                show="*",
                parent=root
            )

            if password is None:
                return False

            if len(password) < 8:
                messagebox.showwarning(
                    "NOVA",
                    "Password must be at least 8 characters.",
                    parent=root
                )
                continue

            confirm = simpledialog.askstring(
                "NOVA Owner Setup",
                "Confirm owner password:",
                show="*",
                parent=root
            )

            if confirm is None:
                return False

            if password != confirm:
                messagebox.showwarning(
                    "NOVA",
                    "Passwords do not match.",
                    parent=root
                )
                continue

            PASSWORD_FILE.write_text(
                hash_password(password),
                encoding="utf-8"
            )

            messagebox.showinfo(
                "NOVA",
                "Owner authentication created successfully.",
                parent=root
            )

            return True

    finally:
        root.destroy()


def authenticate():
    if not PASSWORD_FILE.exists():
        if not setup_owner():
            return False

    root = create_hidden_root()

    try:
        saved_hash = PASSWORD_FILE.read_text(
            encoding="utf-8"
        ).strip()

        for attempt in range(3):
            password = simpledialog.askstring(
                "NOVA Owner Verification",
                "Enter NOVA owner password:",
                show="*",
                parent=root
            )

            if password is None:
                return False

            if hash_password(password) == saved_hash:
                messagebox.showinfo(
                    "NOVA",
                    "Owner verified.",
                    parent=root
                )
                return True

            remaining = 2 - attempt

            if remaining > 0:
                messagebox.showwarning(
                    "NOVA",
                    f"Incorrect password.\n"
                    f"Attempts remaining: {remaining}",
                    parent=root
                )

        messagebox.showerror(
            "NOVA",
            "ACCESS LOCKED.",
            parent=root
        )

        return False

    finally:
        root.destroy()


if __name__ == "__main__":
    if authenticate():
        print("Access granted.")
    else:
        print("Access denied.")