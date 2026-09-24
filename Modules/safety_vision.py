import cv2
import time
from datetime import datetime


WINDOW_NAME = "JARVIS Safety Vision"

# Visual objects that should trigger a caution message.
# This is deliberately conservative: it does NOT identify people
# as attackers and does NOT make a medical diagnosis.
CAUTION_OBJECTS = {
    "fire",
    "smoke",
    "knife",
    "gun",
    "weapon",
    "explosive",
}


def security_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("safety.log", "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {message}\n")


def show_warning(message):
    print("\n" + "=" * 50)
    print("JARVIS SAFETY ALERT")
    print(message)
    print("=" * 50)

    security_log(message)


def start_safety_camera(camera_index=0):
    camera = cv2.VideoCapture(camera_index)

    if not camera.isOpened():
        print("ERROR: Camera could not be opened.")
        return

    print("JARVIS Safety Vision started.")
    print("Press Q to stop.")

    last_alert = 0

    while True:
        success, frame = camera.read()

        if not success:
            print("ERROR: Could not read camera frame.")
            break

        # Camera feed is displayed.
        # Object recognition will be added in the next stage.
        cv2.putText(
            frame,
            "JARVIS SAFETY VISION",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
        )

        cv2.putText(
            frame,
            "Monitoring...",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )

        cv2.imshow(WINDOW_NAME, frame)

        # Prevent accidental repeated alerts.
        current_time = time.time()

        if current_time - last_alert > 10:
            # Placeholder safety check.
            # No threat is claimed without a vision model.
            last_alert = current_time

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

    print("JARVIS Safety Vision stopped.")


if __name__ == "__main__":
    start_safety_camera()
