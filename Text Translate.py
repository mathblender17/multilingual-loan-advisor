import requests
from langdetect import detect
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# API Configuration
SARVAM_API_KEY = os.getenv('SARVAM_API_KEY', "44e5ae09-d0e2-4525-9e16-bda924398004")  # Fallback to default key if not in .env
API_URL = "https://api.sarvam.ai/translate"

def get_language_code(detected_lang):
    """Convert langdetect codes to Sarvam AI language codes"""
    language_mapping = {
        'en': 'en-IN',
        'hi': 'hi-IN',
        'ta': 'ta-IN',
        'te': 'te-IN',
        'kn': 'kn-IN',
        'ml': 'ml-IN',
        'bn': 'bn-IN',
        'gu': 'gu-IN',
        'mr': 'mr-IN',
        'pa': 'pa-IN'
    }
    return language_mapping.get(detected_lang, 'en-IN')

def translate_text(text, target_lang_code=None):
    """
    Translate text to specified target language or auto-detect and translate
    Returns both the translated text and the detected source language
    """
    try:
        # Detect the language of input text
        detected_lang = detect(text)
        source_lang = get_language_code(detected_lang)
        
        # If target language not specified, determine based on source
        if not target_lang_code:
            # If source is English, default to Hindi, otherwise English
            target_lang_code = 'hi-IN' if detected_lang == 'en' else 'en-IN'
        
        payload = {
            "enable_preprocessing": True,
            "model": "mayura:v1",
            "mode": "classic-colloquial",  # Using classic-colloquial for balanced formality
            "speaker_gender": "Female",
            "target_language_code": target_lang_code,
            "source_language_code": source_lang,
            "numerals_format": "international",
            "input": text,
            "output_script": "fully-native"  # Using native script for better readability
        }
        
        headers = {
            "api-subscription-key": SARVAM_API_KEY,
            "Content-Type": "application/json"
        }
        
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        
        return {
            'translated_text': response.json().get('translated_text', ''),
            'source_language': source_lang,
            'target_language': target_lang_code
        }
        
    except Exception as e:
        print(f"Translation error: {e}")
        return None

def chat_assistant():
    """Interactive chat assistant with multilingual support"""
    print("Welcome! You can type in any supported language, and I'll respond accordingly.")
    print("Available languages: English, Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali, Gujarati, Marathi, Punjabi")
    print("Type 'quit' to exit or 'change language' to set a specific target language.")
    
    current_target_lang = None  # Default to auto-detection
    
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
            
        if user_input.lower() == 'change language':
            print("\nSelect target language:")
            print("1. English (en-IN)")
            print("2. Hindi (hi-IN)")
            print("3. Tamil (ta-IN)")
            print("4. Telugu (te-IN)")
            print("5. Kannada (kn-IN)")
            print("6. Malayalam (ml-IN)")
            print("7. Bengali (bn-IN)")
            print("8. Gujarati (gu-IN)")
            print("9. Marathi (mr-IN)")
            print("10. Punjabi (pa-IN)")
            
            lang_choice = input("Enter number (1-10): ").strip()
            lang_codes = {
                '1': 'en-IN', '2': 'hi-IN', '3': 'ta-IN', 
                '4': 'te-IN', '5': 'kn-IN', '6': 'ml-IN',
                '7': 'bn-IN', '8': 'gu-IN', '9': 'mr-IN',
                '10': 'pa-IN'
            }
            current_target_lang = lang_codes.get(lang_choice)
            if current_target_lang:
                print(f"Target language set to: {current_target_lang}")
            continue
            
        if not user_input:
            continue
            
        # Translate user input
        translation_result = translate_text(user_input, current_target_lang)
        
        if translation_result:
            # Get English version of the text for processing
            english_text = user_input if translation_result['source_language'] == 'en-IN' else translation_result['translated_text']
            
            # Create response in English
            english_response = f"I understood your message: {english_text}"
            
            # Translate response back to source language if needed
            if translation_result['source_language'] != 'en-IN' or current_target_lang:
                response_translation = translate_text(english_response, 
                    current_target_lang or translation_result['source_language'])
                if response_translation:
                    final_response = response_translation['translated_text']
                else:
                    final_response = "Sorry, there was an error processing your request."
            else:
                final_response = english_response
                
            print(f"Assistant: {final_response}")
        else:
            print("Assistant: Sorry, I couldn't process that message.")

if __name__ == "__main__":
    chat_assistant()
