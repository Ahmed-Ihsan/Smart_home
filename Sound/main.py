# import speech_recognition as sr
# import pyttsx3
# import webbrowser

# class PatientAssistant:
#     def __init__(self):

#         self.recognizer = sr.Recognizer()
#         self.engine = pyttsx3.init()

#     def speak(self, text):
#         self.engine.say(text)
#         self.engine.runAndWait()

#     def open_webpage(self, query):
#         url = f"https://www.google.com/search?q={query}"
#         webbrowser.open(url)

#     def remind_medication(self):
#         self.speak("Don't forget to take your medication.")

#     def call_ambulance(self):
#         self.speak("Calling for an ambulance.")

#     def call_police(self):
#         self.speak("Calling the police.")


#     def order_food(self):
#         self.speak("Ordering food.")

#     def request_delivery(self):
#         self.speak("Requesting a delivery.")

#     # الإضافات الجديدة
#     def ask_assistance(self):
#         self.speak("Assistance is on the way. Stay calm.")

#     def check_blood_sugar(self):
#         self.speak("Checking your blood sugar level.")

#     def adjust_lighting(self):
#         self.speak("Adjusting the room lighting.")

#     def play_music(self):

#         self.speak("Playing some relaxing music.")

# def main():
#     assistant = PatientAssistant()

#     while True:
#         try:
#             with sr.Microphone() as source:
#                 print("Listening...")
#                 audio = assistant.recognizer.listen(source)
#                 command = assistant.recognizer.recognize_google(audio, language="ar")
#                 print("You said:", command)

#                 if "ambulance" in command:
#                     assistant.call_ambulance()
#                 elif "police" in command:
#                     assistant.call_police()

#                 elif "food" in command:
#                     assistant.order_food()
#                 elif "delivery" in command:
#                     assistant.request_delivery()
#                 elif "help" in command:
#                     assistant.ask_assistance()
#                 elif "medication" in command:
#                     assistant.remind_medication()
#                 elif "sugar" in command:
#                     assistant.check_blood_sugar()
#                 elif "lighting" in command:
#                     assistant.adjust_lighting()
#                 elif "music" in command:
#                     assistant.play_music()
#                 else:
#                     assistant.speak("Sorry, I didn't understand.")
#         except sr.UnknownValueError:
#             print("Sorry, I didn't catch that. Please try again.")
#         except sr.RequestError:

#             print("Sorry, I'm having trouble connecting to the server. Please try again later.")

# if __name__ == "__main__":
#     assistant = PatientAssistant()
#     assistant.speak("اهلا وسهلا hi ")
#     # main()

from gtts import gTTS
import io
import pygame

class TextToSpeech:
    def __init__(self, text, language='ar'):
        self.text = text
        self.language = language
        self.audio_data = io.BytesIO()
        self.initialize_audio()
    
    def initialize_audio(self):
        tts = gTTS(text=self.text, lang=self.language)
        tts.write_to_fp(self.audio_data)
        self.audio_data.seek(0)
        pygame.mixer.init()
    
    def play_audio(self):
        pygame.mixer.music.load(self.audio_data)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

if __name__ == "__main__":
    arabic_text = "مرحبًا، كيف يمكنني مساعدتك؟"
    tts = TextToSpeech(arabic_text)
    tts.play_audio()


# import pyttsx3

# engine = pyttsx3.init()
# voices = engine.getProperty("voices")

# for voice in voices:
#     print(voice.name)
    
# def text_to_speech(text, voice_name="Hoda"):
#     engine = pyttsx3.init()
#     voices = engine.getProperty('voices')
#     for voice in voices:
#         if voice_name in voice.name:
#             engine.setProperty('voice', voice.id)
#             break
#     engine.say(text)
#     engine.runAndWait()

# if __name__ == "__main__":
#     arabic_text = "Hi how are you"
#     text_to_speech(arabic_text, "Zira")
