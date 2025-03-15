import requests
import sounddevice as sd
import wave
import numpy as np
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
SARVAM_API_KEY = os.getenv('SARVAM_API_KEY', "44e5ae09-d0e2-4525-9e16-bda924398004")  # Fallback to default key
API_URL = "https://api.sarvam.ai/speech-to-text"

class SpeechToText:
    def __init__(self):
        self.api_url = API_URL
        self.api_key = SARVAM_API_KEY

    def list_audio_devices(self):
        """List all available audio input devices"""
        print("\nAvailable audio input devices:")
        devices = sd.query_devices()
        input_devices = []
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:  # Only show input devices
                print(f"{i}: {device['name']} (inputs: {device['max_input_channels']})")
                input_devices.append(i)
        return input_devices

    def get_default_device(self):
        """Get the default input device"""
        try:
            device = sd.query_devices(kind='input')
            return device['index']
        except:
            return None

    def record_audio(self, duration=5, sample_rate=16000, device=None):
        """Record audio from selected device"""
        try:
            # If no device specified, show available devices and let user choose
            if device is None:
                input_devices = self.list_audio_devices()
                if not input_devices:
                    print("No input devices found!")
                    return None
                
                default_device = self.get_default_device()
                if default_device is not None:
                    print(f"\nDefault input device: {default_device}")
                
                device_choice = input("\nSelect input device number (or press Enter for default): ").strip()
                if device_choice:
                    device = int(device_choice)
                else:
                    device = default_device

            # Test device before recording
            try:
                sd.check_input_settings(device=device, channels=1, samplerate=sample_rate)
                print(f"\nUsing device: {sd.query_devices(device)['name']}")
            except Exception as e:
                print(f"Error with selected device: {e}")
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
                device=device,
                blocking=True
            )
            
            print("✅ Recording finished!")
            
            # Save recording
            output_path = "recorded_audio.wav"
            
            with wave.open(output_path, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)  # 16-bit audio
                wf.setframerate(sample_rate)
                wf.writeframes(recording.tobytes())
                
            print(f"Audio saved as: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"\n❌ Error recording audio: {e}")
            print("\nTroubleshooting tips:")
            print("1. Make sure you have a working microphone connected")
            print("2. Try selecting a different input device")
            print("3. Check if your microphone is being used by another application")
            print("4. Verify your system recognizes the microphone")
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
    try:
        stt = SpeechToText()
    except ValueError as e:
        print(f"Error: {e}")
        return
    
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
