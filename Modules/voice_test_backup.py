import datetime
import speech_recognition as sr
import pyttsx3


recognizer = sr.Recognizer()
speaker = pyttsx3.init()

# NOVA ki speaking speed
speaker.setProperty("rate", 165)


def speak(text):
    print(f"NOVA: {text}")
    speaker.say(text)
    speaker.runAndWait()


def listen():
    with sr.Microphone() as source:
        print("\n🎤 NOVA sun rahi hai...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )
        except sr.WaitTimeoutError:
            print("Koi awaaz nahi mili.")
            return None

    try:
        # Urdu recognition
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
        print(f"Speech service error: {error}")
        return None


def process_voice_command(command):
    if not command:
        return True

    # Exit commands
    if any(word in command for word in [
        "exit",
        "stop",
        "band ho jao",
        "band karo",
        "ختم",
        "بند ہو جاؤ"
    ]):
        speak("Theek hai. Main band ho rahi hoon.")
        return False

    # Time command
    if any(word in command for word in [
        "time",
        "waqt",
        "kitne baje",
        "kya time",
        "کیا وقت",
        "کتنے بجے"
    ]):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"Abhi {current_time} ho rahe hain.")
        return True

    # Greeting
    if any(word in command for word in [
        "hello",
        "hi",
        "salam",
        "assalam",
        "ہیلو",
        "سلام"
    ]):
        speak("Assalam o Alaikum. Main NOVA hoon. Aap mujh se baat kar sakte hain.")
        return True

    # Name
    if any(word in command for word in [
        "mera naam",
        "میرا نام"
    ]):
        speak("Aap ka naam Kashan hai.")
        return True

    speak("Main ne aap ki baat suni, lekin abhi is command ka jawab mere paas nahi hai.")
    return True


def voice_chat():
    speak("NOVA voice system ready hai. Aap mujh se baat kar sakte hain.")

    while True:
        command = listen()

        if not process_voice_command(command):
            break


if __name__ == "__main__":
    voice_chat()
