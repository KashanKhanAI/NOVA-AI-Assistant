import cv2
from .permissions import check_permission


def start_camera():
    if not check_permission("camera"):
        print("NOVA: Camera permission is OFF.")
        return False

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("NOVA: Camera open nahi ho saka.")
        return False

    print("NOVA: Camera successfully connected.")
    print("NOVA: Camera band karne ke liye Q dabayein.")

    while True:
        success, frame = camera.read()

        if not success:
            print("NOVA: Camera frame nahi mil raha.")
            break

        cv2.imshow("NOVA Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

    print("NOVA: Camera stopped.")
    return True


if __name__ == "__main__":
    start_camera()
