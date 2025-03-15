import requests
import json
import os
from dotenv import load_dotenv
import PyPDF2

# Load environment variables
load_dotenv()

# API Configuration
SARVAM_API_KEY = os.getenv('SARVAM_API_KEY', "44e5ae09-d0e2-4525-9e16-bda924398004")
API_URL = "https://api.sarvam.ai/translate"

class DocumentTranslator:
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

    def read_pdf(self, pdf_path):
        """Read content from PDF file"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
                    
        except Exception as e:
            print(f"❌ Error reading PDF: {e}")
            return None

    def translate_text(self, text, language):
        """Translate text using Sarvam AI API"""
        try:
            # Get the correct language code
            language = language.lower()
            output_lang = self.language_codes.get(language)
            
            if not output_lang:
                print(f"❌ Unsupported language. Supported languages are: {', '.join(self.language_codes.keys())}")
                return None

            # Prepare headers and data
            headers = {
                'api-subscription-key': self.api_key,
                'Content-Type': 'application/json'
            }

            data = {
                'input': text,
                'source_language_code': 'en-IN',
                'target_language_code': output_lang,
                'model': 'mayura:v1',
                'enable_preprocessing': True
            }

            # Make API request
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data
            )

            if response.status_code == 200:
                result = response.json()
                return result.get('translated_text')
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"Response: {response.text}")
                return None

        except Exception as e:
            print(f"❌ Error during translation: {e}")
            return None

def main():
    translator = DocumentTranslator()
    
    while True:
        print("\n=== Document Translation Chat ===")
        print("1. Read and translate document")
        print("2. Exit")
        
        choice = input("\nEnter your choice (1-2): ").strip()
        
        if choice == "2":
            print("Goodbye!")
            break
            
        elif choice == "1":
            # Get PDF path
            pdf_path = input("\nEnter path to PDF file: ").strip()
            
            # Get desired language
            print("\nSupported languages: hindi, bengali, gujarati, kannada, malayalam, marathi, odia, punjabi, tamil, telugu")
            language = input("Enter desired language: ").strip()
            
            # Read PDF content
            print("\nReading document...")
            content = translator.read_pdf(pdf_path)
            
            if content:
                print("\nOriginal content:")
                print("-" * 50)
                print(content)
                print("-" * 50)
                
                # Translate content
                print(f"\nTranslating to {language}...")
                translated_text = translator.translate_text(content, language)
                
                if translated_text:
                    print("\nTranslated content:")
                    print("-" * 50)
                    print(translated_text)
                    print("-" * 50)
            
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
