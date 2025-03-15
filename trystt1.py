import requests
from langdetect import detect
import json

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
        'pa': 'pa-IN',
        # Add more language mappings as needed
    }
    return language_mapping.get(detected_lang, 'en-IN')

def translate_text(text):
    """
    Automatically detect language and translate between English and Indic languages
    Returns both the translated text and the detected source language
    """
    url = "https://api.sarvam.ai/translate"
    
    try:
        # Detect the language of input text
        detected_lang = detect(text)
        source_lang = get_language_code(detected_lang)
        
        # If text is in English, translate to Hindi (default Indic language)
        # If text is in an Indic language, translate to English
        target_lang = 'hi-IN' if detected_lang == 'en' else 'en-IN'
        
        payload = {
            "enable_preprocessing": True,
            "model": "mayura:v1",
            "mode": "formal",
            "speaker_gender": "Female",
            "target_language_code": target_lang,
            "source_language_code": source_lang,
            "numerals_format": "native",
            "input": text,
            "output_script": "fully-native"
        }
        
        headers = {
            "api-subscription-key": "44e5ae09-d0e2-4525-9e16-bda924398004",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        return {
            'translated_text': response.json().get('translated_text', ''),
            'source_language': source_lang,
            'target_language': target_lang
        }
        
    except Exception as e:
        print(f"Translation error: {e}")
        return None

def chat_assistant():
    """Interactive chat assistant with automatic language handling"""
    print("Welcome! You can type in any language, and I'll understand and respond accordingly.")
    print("Type 'quit' to exit the conversation.")
    
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
            
        if not user_input:
            continue
            
        # Translate user input if it's not in English
        translation_result = translate_text(user_input)
        
        if translation_result:
            # If original text was in English, use it directly
            # Otherwise, use the translated English text
            english_text = user_input if translation_result['source_language'] == 'en-IN' else translation_result['translated_text']
            
            # Here you would process the English text with your AI agent
            # For this example, we'll just create a simple response
            english_response = f"I understood your message: {english_text}"
            
            # If original input wasn't in English, translate the response back
            if translation_result['source_language'] != 'en-IN':
                response_translation = translate_text(english_response)
                if response_translation:
                    final_response = response_translation['translated_text']
                else:
                    final_response = "Sorry, there was an error processing your request."
            else:
                final_response = english_response
                
            print(f"Assistant: {final_response}")
        else:
            print("Assistant: Sorry, I couldn't process that message.")

# Install required package:
# pip install langdetect requests

if __name__ == "__main__":
    chat_assistant()
