import datetime
import speech_recognition as sr
import pyttsx3


recognizer = sr.Recognizer()
speaker = pyttsx3.init()

speaker.setProperty("rate", 165)


def speak(text):
    print(f"NOVA: {text}")
    speaker.say(text)
    speaker.runAndWait()


def listen():
    with sr.Microphone() as source:
        print("\n🎤 NOVA sun rahi hai...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

        except sr.WaitTimeoutError:
            print("NOVA: Koi awaaz nahi mili.")
            return None

    try:
        text = recognizer.recognize_google(
            audio,
            language="ur-PK"
        )

        print(f"You: {text}")
        return text.lower().strip()

    except sr.UnknownValueError:
        print("NOVA: Mujhe samajh nahi aaya.")
        return None

    except sr.RequestError as error:
        print(f"NOVA: Speech service error: {error}")
        return None


def process_voice_command(command):

    if not command:
        return True

    # EXIT
    exit_words = [
        "exit",
        "stop",
        "band ho jao",
        "band karo",
        "ختم",
        "بند ہو جاؤ"
    ]

    if any(word in command for word in exit_words):
        speak("Theek hai. Main band ho rahi hoon.")
        return False

    # TIME
    time_words = [
        "time",
        "waqt",
        "وقت",
        "kitne baje",
        "کتنے بجے",
        "kya time hai",
        "کیا ٹائم ہے",
        "time batao",
        "ٹائم بتاؤ",
        "waqt batao",
        "وقت بتاؤ"
    ]

    if any(word in command for word in time_words):

        now = datetime.datetime.now()

        hour = now.strftime("%I").lstrip("0")
        minute = now.strftime("%M")

        if minute == "00":
            answer = f"Abhi {hour} bajay hain."
        else:
            answer = f"Abhi {hour} baj kar {minute} minute hue hain."

        speak(answer)
        return True

    # GREETING
    greeting_words = [
        "hello",
        "hi",
        "salam",
        "assalam",
        "ہیلو",
        "سلام"
    ]

    if any(word in command for word in greeting_words):
        speak(
            "Wa Alaikum Assalam. "
            "Main NOVA hoon. "
            "Aap mujh se baat kar sakte hain."
        )
        return True

    # NAME
    name_words = [
        "mera naam kya hai",
        "mera naam",
        "میرا نام کیا ہے",
        "میرا نام"
    ]

    if any(word in command for word in name_words):
        speak("Aap ka naam Kashan hai.")
        return True

    # BASIC CONVERSATION
    if "kaisi ho" in command or "کیسی ہو" in command:
        speak(
            "Main bilkul theek hoon. "
            "Aap bataiye, main aap ki kya madad kar sakti hoon?"
        )
        return True

    speak(
        "Main ne aap ki baat suni hai, "
        "lekin is command ka jawab abhi mere paas nahi hai."
    )

    return True


def voice_chat():

    speak(
        "NOVA voice system ready hai. "
        "Aap mujh se baat kar sakte hain."
    )

    while True:

        command = listen()

        if not process_voice_command(command):
            break


if __name__ == "__main__":
    voice_chat()
