import cv2


def test_camera():
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("NOVA: Camera open nahi ho saka.")
        return

    print("NOVA: Camera successfully connected.")
    print("NOVA: Camera window band karne ke liye Q dabayein.")

    while True:
        success, frame = camera.read()

        if not success:
            print("NOVA: Camera frame nahi mil raha.")
            break

        cv2.imshow("NOVA Camera Test", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()
    print("NOVA: Camera test stopped.")


if __name__ == "__main__":
    test_camera()
