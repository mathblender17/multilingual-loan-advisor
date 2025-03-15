import requests
import base64
import io
import sounddevice as sd
import numpy as np
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# API Configuration
SARVAM_API_KEY = os.getenv('SARVAM_API_KEY', "44e5ae09-d0e2-4525-9e16-bda924398004")
API_URL = "https://api.sarvam.ai/text-to-speech"

class TextToSpeech:
    def __init__(self):
        self.api_url = API_URL
        self.api_key = SARVAM_API_KEY
        self.language_codes = {
            'hindi': 'hi-IN',
            'bengali': 'bn-IN',
            'gujarati': 'gu-IN',
            'kannada': 'kn-IN',
            'malayalam': 'ml-IN',
            'marathi': 'mr-IN',
            'odia': 'od-IN',
            'punjabi': 'pa-IN',
            'tamil': 'ta-IN',
            'telugu': 'te-IN'
        }
        self.sample_rate = 22050

    def play_audio(self, audio_data):
        """Play audio data directly"""
        try:
            # Convert audio data to numpy array
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            
            # Play the audio
            sd.play(audio_array, self.sample_rate)
            sd.wait()  # Wait until audio is finished playing
            
        except Exception as e:
            print(f"❌ Error playing audio: {e}")

    def speak(self, text, language):
        """Convert text to speech and play it directly"""
        try:
            # Get the correct language code
            language = language.lower()
            target_lang = self.language_codes.get(language)
            
            if not target_lang:
                print(f"❌ Unsupported language. Supported languages are: {', '.join(self.language_codes.keys())}")
                return False

            # Split text into chunks of 500 characters
            chunks = [text[i:i+500] for i in range(0, len(text), 500)]

            # Prepare headers
            headers = {
                "Content-Type": "application/json",
                "api-subscription-key": self.api_key
            }

            # Process and play each chunk
            for i, chunk in enumerate(chunks):
                payload = {
                    "inputs": [chunk],
                    "target_language_code": target_lang,
                    "speaker": "meera",
                    "model": "bulbul:v1",
                    "pitch": 0,
                    "pace": 1.0,
                    "loudness": 1.0,
                    "speech_sample_rate": self.sample_rate,
                    "enable_preprocessing": True
                }

                print(f"Converting chunk {i+1}/{len(chunks)}...")
                response = requests.post(self.api_url, json=payload, headers=headers)

                if response.status_code == 200:
                    # Decode and play audio
                    audio_data = base64.b64decode(response.json()["audios"][0])
                    print("🔊 Playing audio...")
                    self.play_audio(audio_data)
                else:
                    print(f"❌ API Error: {response.status_code}")
                    print(f"Response: {response.text}")
                    return False

            return True

        except Exception as e:
            print(f"❌ Error converting text to speech: {e}")
            return False

def main():
    tts = TextToSpeech()
    
    while True:
        print("\n=== Text to Speech Converter ===")
        print("1. Speak text")
        print("2. Exit")
        
        choice = input("\nEnter your choice (1-2): ").strip()
        
        if choice == "2":
            print("Goodbye!")
            break
            
        elif choice == "1":
            # Get text input
            print("\nEnter the text to speak (press Enter twice to finish):")
            lines = []
            while True:
                line = input()
                if line:
                    lines.append(line)
                else:
                    break
            text = "\n".join(lines)
            
            # Get desired language
            print("\nSupported languages: hindi, bengali, gujarati, kannada, malayalam, marathi, odia, punjabi, tamil, telugu")
            language = input("Enter desired language: ").strip()
            
            # Convert and play
            tts.speak(text, language)
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
