import speech_recognition as sr

MIC_NAME = "Microphone (Realtek High Definition Audio)"


def listen():
    recognizer = sr.Recognizer()

    # Microphone find karo
    mic_index = None

    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        if name == MIC_NAME:
            mic_index = index
            break

    if mic_index is None:
        print("NOVA: Microphone not found.")
        return ""

    try:
        with sr.Microphone(device_index=mic_index) as source:
            print("NOVA: Listening... Speak now!")

            # Microphone threshold
            recognizer.energy_threshold = 300
            recognizer.dynamic_energy_threshold = False

            # Speech capture
            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=8
            )

        print("NOVA: Processing...")

        text = recognizer.recognize_google(
            audio,
            language="en-US"
        )

        print("You:", text)
        return text

    except sr.WaitTimeoutError:
        print("NOVA: No speech detected.")
        return ""

    except sr.UnknownValueError:
        print("NOVA: Speech detected, but I couldn't understand it.")
        return ""

    except sr.RequestError as error:
        print("NOVA: Speech service error:", error)
        return ""

    except Exception as error:
        print("NOVA: Voice error:", error)
        return ""


if __name__ == "__main__":
    listen()
import speech_recognition as sr

MIC_INDEX = 1


def listen():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone(device_index=MIC_INDEX) as source:
            print("NOVA: Listening... Speak now!")

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=5
            )

        print("NOVA: Processing...")

        text = recognizer.recognize_google(
            audio,
            language="en-US"
        )

        print("You:", text)
        return text

    except sr.WaitTimeoutError:
        print("NOVA: No speech detected.")
        return ""

    except sr.UnknownValueError:
        print("NOVA: Speech detected, but I couldn't understand it.")
        return ""

    except sr.RequestError as error:
        print("NOVA: Speech service error:", error)
        return ""

    except Exception as error:
        print("NOVA: Voice error:", error)
        return ""


if __name__ == "__main__":
    listen()
