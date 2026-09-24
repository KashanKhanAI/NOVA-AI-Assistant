import speech_recognition as sr

MIC_NAME = "Microphone (Realtek High Definition Audio)"


def listen():
    recognizer = sr.Recognizer()

    mic_index = None

    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        if name == MIC_NAME:
            mic_index = index
            break

    if mic_index is None:
        print("NOVA: Microphone not found.")
        return ""

    with sr.Microphone(device_index=mic_index) as source:
        print("NOVA: Adjusting microphone...")
        recognizer.adjust_for_ambient_noise(source, duration=2)

        print("NOVA: Listening... Speak now!")

        try:
            audio = recognizer.listen(
                source,
                timeout=15,
                phrase_time_limit=10
            )
        except sr.WaitTimeoutError:
            print("NOVA: No speech detected.")
            return ""

    try:
        text = recognizer.recognize_google(
            audio,
            language="en-US"
        )

        print("You:", text)
        return text

    except sr.UnknownValueError:
        print("NOVA: Speech was detected, but I couldn't understand it.")
        return ""

    except sr.RequestError as error:
        print("NOVA: Internet speech service error:", error)
        return ""


if __name__ == "__main__":
    listen()
