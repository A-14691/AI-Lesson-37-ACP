import speech_recognition as sr
import pyttsx3
from deep_translator import GoogleTranslator

LANGUAGES = {
    "1": ("Hindi", "hi"), "2": ("Tamil", "ta"), "3": ("Telugu", "te"),
    "4": ("Bengali", "bn"), "5": ("Marathi", "mr"), "6": ("Gujarati", "gu"),
    "7": ("Malayalam", "ml"), "8": ("Punjabi", "pa")
}


def display_language_options():
    print("\n🌍 Available translation languages:")
    for number, (name, code) in LANGUAGES.items():
        print(f"{number}. {name} ({code})")

    while True:
        choice = input("Please select the target language number (1-8): ").strip()
        if choice in LANGUAGES:
            return LANGUAGES[choice][1]
        print("Invalid choice. Please enter a number from 1 to 8.")


def speech_to_text(timeout=5, phrase_time_limit=10):
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("\n🎤 Adjusting for background noise... Please wait.")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("🎤 Please speak now in English...")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

        print("🔎 Recognizing speech...")
        text = recognizer.recognize_google(audio, language="en-US")
        print(f"You said: {text}")
        return text.strip()

    except sr.WaitTimeoutError:
        print("No speech was detected before the microphone timed out.")
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError as error:
        print(f"Speech recognition service error: {error}")
    except OSError as error:
        print(f"Could not access the microphone: {error}")
    except Exception as error:
        print(f"An unexpected speech recognition error occurred: {error}")
    return ""


def translate_text(text, target_language="hi"):
    if not text:
        return ""

    print(f"Translating English to {target_language}...")
    try:
        translated_text = GoogleTranslator(source="auto", target=target_language).translate(text)
        if not translated_text:
            raise ValueError("The translation service returned an empty result.")

        print(f"English: {text}")
        print(f"Translated text: {translated_text}")
        return translated_text
    except Exception as error:
        print(f"Translation failed: {error}")
        return ""


def speak(text, language="en"):
    if not text:
        return False

    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        engine.setProperty("volume", 0.9)
        voices = engine.getProperty("voices") or []

        if voices:
            voice_keywords = {
                "hi": "hindi", "ta": "tamil", "te": "telugu",
                "bn": "bengali", "mr": "marathi", "gu": "gujarati",
                "ml": "malayalam", "pa": "punjabi", "en": "english"
            }
            keyword = voice_keywords.get(language, "")
            matching_voice = next(
                (voice for voice in voices
                 if keyword.lower() in (voice.name + " " + voice.id).lower()),
                None
            )
            engine.setProperty("voice", (matching_voice or voices[0]).id)

        engine.say(text)
        engine.runAndWait()
        return True
    except Exception as error:
        print(f"Text-to-speech failed: {error}")
        print("Translated text:", text)
        return False


def main():
    print("=== English Speech Translator ===")
    target_language = display_language_options()
    original_text = speech_to_text()

    if not original_text:
        print("Translation was cancelled because no valid speech was captured.")
        return

    translated_text = translate_text(original_text, target_language)
    if not translated_text:
        print("Translation was cancelled because translation failed.")
        return

    if speak(translated_text, target_language):
        print("✅ Translation spoken successfully!")
    else:
        print("Translation completed, but speech output was unavailable.")


if __name__ == "__main__":
    main()
