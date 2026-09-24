from datetime import datetime
from pathlib import Path


class SecurityLogger:
    def __init__(self, log_file=None):
        if log_file is None:
            base_dir = Path(__file__).resolve().parent.parent
            log_file = base_dir / "Logs" / "security.log"

        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def write(self, event, details=""):
        timestamp = datetime.now().isoformat(timespec="seconds")

        line = f"[{timestamp}] {event}"

        if details:
            line += f" | {details}"

        with self.log_file.open(
            "a",
            encoding="utf-8"
        ) as file:
            file.write(line + "\n")
