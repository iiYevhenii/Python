from googletrans import Translator, LANGUAGES

def CodeLang(lang: str) -> str:
    lang_lower = lang.lower()
    
    if lang_lower in LANGUAGES:
        return LANGUAGES[lang_lower].capitalize()
    
    for code, name in LANGUAGES.items():
        if name.lower() == lang_lower:
            return code
            
    return "Error: Language not found"

def TransLate(text: str, lang: str) -> str:
    translator = Translator()
    try:
        dest_code = lang.lower()
        if dest_code not in LANGUAGES:
            dest_code = CodeLang(lang)
            if dest_code == "Error: Language not found":
                return "Error: Invalid language setting"

        result = translator.translate(text, dest=dest_code)
        translated_text = result.text
        
        if text and text[0].isupper() and translated_text:
            translated_text = translated_text[0].upper() + translated_text[1:]
            
        return translated_text
    except Exception as e:
        return f"Translation error: {e}"

def LangDetect(txt: str) -> str:
    translator = Translator()
    try:
        result = translator.detect(txt)
        confidence = result.confidence if result.confidence is not None else 1
        return f"Detected(lang={result.lang}, confidence={confidence})"
    except Exception as e:
        return f"Language detection error: {e}"

if __name__ == "__main__":
    current_lang = None
    
    while True:
        print("\nMenu")
        print("1. Select language")
        print("2. Enter text")
        print("0. Exit")
        
        choice = input("Select: ")
        
        if choice == '1':
            lang_input = input("Enter the translation language (code or name): ")
            if CodeLang(lang_input) == "Error: Language not found":
                print("Error: No such language found. Please try again.")
            else:
                current_lang = lang_input
                print(f"The language has been successfully set: {current_lang}")
                
        elif choice == '2':
            if current_lang is None:
                print("Error: First select the translation language!")
            else:
                user_txt = input("Enter the text to translate: ")
                print(f"\nSelected language: {current_lang}")
                print("\nTranslation:", TransLate(user_txt, current_lang))
                
        elif choice == '3' or choice == '0':
            print("Exit the program.")
            break
            
        else:
            print("Invalid choice. Please enter 1, 2, or 0.")