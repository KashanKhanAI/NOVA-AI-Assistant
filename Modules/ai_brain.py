import subprocess

JARVIS_EXE = r"C:\Users\sc\AppData\Local\OpenJarvis\OpenJarvis-main\.venv\Scripts\jarvis.exe"

def ask_ai(message):
    result = subprocess.run(
        [JARVIS_EXE, "ask", "-e", "ollama", message],
        capture_output=True,
        text=True,
        timeout=180
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "OpenJarvis failed")

    return result.stdout.strip()
