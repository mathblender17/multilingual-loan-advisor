# speech_to_text.py

import requests
import sounddevice as sd
import wave
import numpy as np
import os
import time
from dotenv import load_dotenv

load_dotenv()

class SpeechToText:
    def __init__(self):
        self.api_url = "https://api.sarvam.ai/speech-to-text"
        self.api_key = os.getenv('SARVAM_API_KEY')
        
        if not self.api_key:
            raise ValueError("API key not found.
            
class SpeechToText:
    def __init__(self):
        self.api_url = "https://api.sarvam.ai/speech-to-text"
        self.api_key = "44e5ae09-d0e2-4525-9e16-bda924398004"

    def list_audio_devices(self):
        """List all available audio devices"""
        print("\nAvailable audio devices:")
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            print(f"{i}: {device['name']} (inputs: {device['max_input_channels']})")

    def setup_audio_device(self):
        """Setup audio device for recording"""
        try:
            # List devices
            self.list_audio_devices()
            
            # Let user select device
            device_id = input("\nSelect input device number (or press Enter for default): ").strip()
            
            if device_id:
                device_info = sd.query_devices(int(device_id), 'input')
                print(f"Using device: {device_info['name']}")
                sd.default.device[0] = int(device_id)
            
            # Test device
            print("\nTesting audio device...")
            with sd.InputStream(channels=1, callback=lambda *args: None):
                time.sleep(0.1)
            print("Audio device test successful!")
            return True
            
        except Exception as e:
            print(f"Error setting up audio device: {e}")
            return False

    def record_audio(self, duration=5, sample_rate=16000):
        """Record audio from microphone"""
        try:
            # Setup device first
            if not self.setup_audio_device():
                return None

            print("\nRecording will start in 3 seconds...")
            for i in range(3, 0, -1):
                print(f"{i}...")
                time.sleep(1)
                
            print("🎤 Recording... Speak now!")
            
            # Record audio
            recording = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                dtype='int16',
                blocking=True
            )
            
            print("✅ Recording finished!")
            
            # Save recording
            output_path = "recorded_audio.wav"
            
            # Save as WAV file
            with wave.open(output_path, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                wf.writeframes(recording.tobytes())
                
            print(f"Audio saved as: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Error recording audio: {e}")
            print("\nTroubleshooting tips:")
            print("1. Make sure your microphone is connected and working")
            print("2. Grant microphone permissions to your terminal/IDE")
            print("3. Try selecting a different input device")
            return None

    def transcribe_audio(self, audio_file_path, language_code="hi-IN"):
        """Transcribe audio file to text"""
        try:
            print(f"\nTranscribing audio file: {audio_file_path}")
            
            if not os.path.exists(audio_file_path):
                print("❌ Audio file not found!")
                return None
                
            headers = {
                "api-subscription-key": self.api_key
            }
            
            data = {
                "language_code": language_code,
                "model": "saarika:v2",
                "with_timestamps": False
            }
            
            with open(audio_file_path, 'rb') as audio_file:
                files = {
                    'file': ('audio.wav', audio_file, 'audio/wav')
                }
                
                print("Sending request to Sarvam AI API...")
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    data=data,
                    files=files
                )
                
                print(f"Response status: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    transcript = result.get('transcript')
                    print("\n✅ Transcription successful!")
                    return transcript
                else:
                    print(f"❌ API Error: {response.status_code}")
                    print(f"Response: {response.text}")
                    return None
                    
        except Exception as e:
            print(f"❌ Error in transcription: {e}")
            return None

def main():
    """Test the Speech-to-Text functionality"""
    stt = SpeechToText()
    
    while True:
        print("\n=== Speech-to-Text Demo ===")
        print("1. Record and transcribe")
        print("2. Transcribe existing audio file")
        print("3. List audio devices")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "4":
            print("Goodbye!")
            break
            
        if choice == "3":
            stt.list_audio_devices()
            
        elif choice == "1":
            print("\nSelect language:")
            print("1. Hindi (hi-IN)")
            print("2. English (en-IN)")
            print("3. Tamil (ta-IN)")
            print("4. Telugu (te-IN)")
            print("5. Kannada (kn-IN)")
            print("6. Malayalam (ml-IN)")
            
            lang_choice = input("\nSelect language (1-6): ").strip()
            language_codes = {
                "1": "hi-IN",
                "2": "en-IN",
                "3": "ta-IN",
                "4": "te-IN",
                "5": "kn-IN",
                "6": "ml-IN"
            }
            
            language_code = language_codes.get(lang_choice, "hi-IN")
            
            audio_path = stt.record_audio()
            if audio_path:
                transcript = stt.transcribe_audio(audio_path, language_code)
                if transcript:
                    print("\nTranscription:")
                    print(f"'{transcript}'")
                
        elif choice == "2":
            audio_path = input("\nEnter path to audio file (.wav format): ").strip()
            language_code = input("Enter language code (e.g., hi-IN, en-IN): ").strip()
            
            transcript = stt.transcribe_audio(audio_path, language_code)
            if transcript:
                print("\nTranscription:")
                print(f"'{transcript}'")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
