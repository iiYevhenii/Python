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
        print("\n=== Меню ===")
        print("1. Вибір мови")
        print("2. Введення тексту для перекладу")
        print("0. Вихід з програми")
        
        choice = input("Оберіть пункт меню: ")
        
        if choice == '1':
            lang_input = input("Введіть мову перекладу (код або назву): ")
            if CodeLang(lang_input) == "Error: Language not found":
                print("Помилка: Такої мови не знайдено. Спробуйте ще раз.")
            else:
                current_lang = lang_input
                print(f"Мову успішно встановлено: {current_lang}")
                
        elif choice == '2':
            if current_lang is None:
                print("Помилка: Спочатку оберіть мову перекладу (пункт 1)!")
            else:
                user_txt = input("Введіть текст для перекладу: ")
                print(LangDetect(user_txt))
                print("Переклад:", TransLate(user_txt, current_lang))
                
        elif choice == '0':
            print("Вихід з програми. До побачення!")
            break 
            
        else:
            print("Невірний вибір. Будь ласка, введіть 1, 2 або 0.")