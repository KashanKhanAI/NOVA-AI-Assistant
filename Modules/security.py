import hashlib
import secrets
import time


class NovaSecurity:
    def __init__(self, owner_code: str):
        self._owner_code_hash = self._hash(owner_code)
        self._failed_attempts = 0
        self._locked_until = 0.0
        self._authorized_devices = set()

    @staticmethod
    def _hash(value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    def verify_owner(self, code: str) -> bool:
        if time.time() < self._locked_until:
            return False

        if secrets.compare_digest(
            self._owner_code_hash,
            self._hash(code)
        ):
            self._failed_attempts = 0
            return True

        self._failed_attempts += 1

        if self._failed_attempts >= 5:
            self._locked_until = time.time() + 60
            self._failed_attempts = 0

        return False

    def authorize_device(self, device_id: str) -> bool:
        if not device_id:
            return False

        self._authorized_devices.add(device_id)
        return True

    def is_authorized(self, device_id: str) -> bool:
        return device_id in self._authorized_devices

    def revoke_device(self, device_id: str) -> None:
        self._authorized_devices.discard(device_id)
def security_check(command: str) -> bool:
    """
    Basic command safety check for NOVA.
    Returns True for normal commands.
    """
    if not command or not command.strip():
        return False

    return True
