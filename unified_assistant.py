import requests
import sounddevice as sd
import wave
import numpy as np
import os
import time
import base64
import PyPDF2
from langdetect import detect
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
SARVAM_API_KEY = os.getenv('SARVAM_API_KEY', "44e5ae09-d0e2-4525-9e16-bda924398004")

class UnifiedAssistant:
    def __init__(self):
        self.language_codes = {
            'hi': 'hi-IN',
            'bn': 'bn-IN',
            'gu': 'gu-IN',
            'kn': 'kn-IN',
            'ml': 'ml-IN',
            'mr': 'mr-IN',
            'or': 'od-IN',
            'pa': 'pa-IN',
            'ta': 'ta-IN',
            'te': 'te-IN',
            'en': 'en-IN',
            'hindi': 'hi-IN',
            'bengali': 'bn-IN',
            'gujarati': 'gu-IN',
            'kannada': 'kn-IN',
            'malayalam': 'ml-IN',
            'marathi': 'mr-IN',
            'odia': 'od-IN',
            'punjabi': 'pa-IN',
            'tamil': 'ta-IN',
            'telugu': 'te-IN',
            'english': 'en-IN'
        }
        self.sample_rate = 22050
        self.setup_apis()

    def setup_apis(self):
        self.translate_url = "https://api.sarvam.ai/translate"
        self.tts_url = "https://api.sarvam.ai/text-to-speech"
        self.stt_url = "https://api.sarvam.ai/speech-to-text"
        self.doc_url = "https://api.sarvam.ai/parse/translatepdf"

    def get_language_code(self, detected_lang):
        return self.language_codes.get(detected_lang.lower(), 'en-IN')

    def translate_text(self, text):
        try:
            detected_lang = detect(text)
            source_lang = self.get_language_code(detected_lang)
            target_lang = 'hi-IN' if detected_lang == 'en' else 'en-IN'
            
            payload = {
                "input": text,
                "source_language_code": source_lang,
                "target_language_code": target_lang,
                "model": "mayura:v1",
                "enable_preprocessing": True
            }
            
            headers = {
                "api-subscription-key": SARVAM_API_KEY,
                "Content-Type": "application/json"
            }
            
            response = requests.post(self.translate_url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json().get('translated_text', '')
            print(f"Translation error: {response.status_code}")
            print(response.text)
            return None
        except Exception as e:
            print(f"Translation error: {e}")
            return None

    def speak_text(self, text):
        try:
            detected_lang = detect(text)
            target_lang = self.get_language_code(detected_lang)
            
            chunks = [text[i:i+500] for i in range(0, len(text), 500)]
            
            headers = {
                "Content-Type": "application/json",
                "api-subscription-key": SARVAM_API_KEY
            }

            for chunk in chunks:
                payload = {
                    "inputs": [chunk],
                    "target_language_code": target_lang,
                    "speaker": "meera",
                    "model": "bulbul:v1",
                    "speech_sample_rate": self.sample_rate
                }

                response = requests.post(self.tts_url, json=payload, headers=headers)
                if response.status_code == 200:
                    audio_data = base64.b64decode(response.json()["audios"][0])
                    self.play_audio(audio_data)
                else:
                    print(f"TTS error: {response.status_code}")
                    print(response.text)
                    return False
            return True
        except Exception as e:
            print(f"Text-to-speech error: {e}")
            return False

    def play_audio(self, audio_data):
        try:
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            sd.play(audio_array, self.sample_rate)
            sd.wait()
        except Exception as e:
            print(f"Audio playback error: {e}")

    def record_and_transcribe(self, language):
        try:
            audio_path = self.record_audio()
            if audio_path:
                return self.transcribe_audio(audio_path, self.get_language_code(language))
            return None
        except Exception as e:
            print(f"Speech-to-text error: {e}")
            return None

    def record_audio(self, duration=5):
        try:
            print("\nRecording will start in 3 seconds...")
            for i in range(3, 0, -1):
                print(f"{i}...")
                time.sleep(1)
            
            print("🎤 Recording... Speak now!")
            recording = sd.rec(
                int(duration * 16000),
                samplerate=16000,
                channels=1,
                dtype='int16',
                blocking=True
            )
            
            print("✅ Recording finished!")
            
            output_path = "temp_recording.wav"
            with wave.open(output_path, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(16000)
                wf.writeframes(recording.tobytes())
            
            return output_path
        except Exception as e:
            print(f"Recording error: {e}")
            return None

    def transcribe_audio(self, audio_path, language_code):
        try:
            headers = {"api-subscription-key": SARVAM_API_KEY}
            data = {
                "language_code": language_code,
                "model": "saarika:v2"
            }
            
            with open(audio_path, 'rb') as audio_file:
                files = {'file': ('audio.wav', audio_file, 'audio/wav')}
                response = requests.post(self.stt_url, headers=headers, data=data, files=files)
                
            if response.status_code == 200:
                return response.json().get('transcript')
            print(f"STT error: {response.status_code}")
            print(response.text)
            return None
        except Exception as e:
            print(f"Transcription error: {e}")
            return None

    def translate_document(self, pdf_path, target_language):
        try:
            if not os.path.exists(pdf_path):
                print("Error: File not found!")
                return None

            content = self.read_pdf(pdf_path)
            if content:
                detected_lang = detect(content)
                source_lang = self.get_language_code(detected_lang)
                target_lang = self.get_language_code(target_language)
                
                if source_lang == target_lang:
                    print(f"Source and target languages are the same. Please choose a different target language.")
                    return None
                
                print(f"Translating from {detected_lang} to {target_language}...")
                
                payload = {
                    "input": content,
                    "source_language_code": source_lang,
                    "target_language_code": target_lang,
                    "model": "mayura:v1",
                    "enable_preprocessing": True
                }
                
                headers = {
                    "api-subscription-key": SARVAM_API_KEY,
                    "Content-Type": "application/json"
                }
                
                response = requests.post(self.translate_url, json=payload, headers=headers)
                if response.status_code == 200:
                    return response.json().get('translated_text', '')
                print(f"Document translation error: {response.status_code}")
                print(response.text)
            return None
        except Exception as e:
            print(f"Document translation error: {e}")
            return None

    def read_pdf(self, pdf_path):
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                return "\n".join(page.extract_text() for page in pdf_reader.pages)
        except Exception as e:
            print(f"PDF reading error: {e}")
            return None

def main():
    assistant = UnifiedAssistant()
    
    while True:
        print("\n=== Multilingual Assistant ===")
        print("1. Text Translation")
        print("2. Text to Speech")
        print("3. Speech to Text")
        print("4. Document Translation")
        print("5. Exit")
        
        choice = input("\nChoose an option (1-5): ").strip()
        
        if choice == "5":
            print("Goodbye!")
            break
            
        elif choice == "1":
            text = input("\nEnter text to translate: ")
            result = assistant.translate_text(text)
            if result:
                print(f"\nTranslated text: {result}")
                
        elif choice == "2":
            text = input("\nEnter text to speak: ")
            assistant.speak_text(text)
            
        elif choice == "3":
            language = input("\nEnter language you'll speak in: ")
            transcript = assistant.record_and_transcribe(language)
            if transcript:
                print(f"\nTranscription: {transcript}")
                
        elif choice == "4":
            pdf_path = input("\nEnter PDF file path: ")
            target_lang = input("Enter target language: ")
            translated = assistant.translate_document(pdf_path, target_lang)
            if translated:
                print("\nTranslated content:")
                print("-" * 50)
                print(translated)
                print("-" * 50)

if __name__ == "__main__":
    main()
