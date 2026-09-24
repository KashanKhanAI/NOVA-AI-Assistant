import speech_recognition as sr


MIC_INDEX = 1
LISTEN_TIMEOUT = 5
PHRASE_TIME_LIMIT = 7


def listen():
    recognizer = sr.Recognizer()

    # Faster voice detection
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.6
    recognizer.non_speaking_duration = 0.3

    try:
        with sr.Microphone(device_index=MIC_INDEX) as source:

            print("NOVA: Adjusting for background noise...")
            recognizer.adjust_for_ambient_noise(source, duration=0.3)

            print("NOVA: Listening... Speak now!")

            audio = recognizer.listen(
                source,
                timeout=LISTEN_TIMEOUT,
                phrase_time_limit=PHRASE_TIME_LIMIT
            )

        print("NOVA: Processing...")

        # English first
        try:
            text = recognizer.recognize_google(
                audio,
                language="en-US"
            )

        except sr.UnknownValueError:

            # Urdu fallback
            text = recognizer.recognize_google(
                audio,
                language="ur-PK"
            )

        text = text.strip()

        if not text:
            print("NOVA: I couldn't detect a usable command.")
            return ""

        print("You:", text)
        return text

    except sr.WaitTimeoutError:
        print("NOVA: No speech detected.")
        return ""

    except sr.UnknownValueError:
        print("NOVA: I couldn't understand the speech.")
        return ""

    except sr.RequestError as error:
        print("NOVA: Speech service error:", error)
        return ""

    except Exception as error:
        print("NOVA: Voice error:", error)
        return ""


if __name__ == "__main__":
    listen()