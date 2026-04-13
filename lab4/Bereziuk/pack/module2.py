import sys

if sys.version_info >= (3, 13):
    print("Увага: Версія Python >= 3.13. Робота пакета googletrans==3.1.0a0 може бути нестабільною.")

from googletrans import Translator, LANGUAGES

def TransLate(text: str, scr: str, dest: str) -> str:
    try:
        translator = Translator()
        src_lang = scr if scr != 'auto' else 'auto'
        result = translator.translate(text, src=src_lang, dest=dest)
        return result.text
    except Exception as e:
        return f"Помилка: {e}"

def LangDetect(text: str, set: str = "all") -> str:
    try:
        translator = Translator()
        result = translator.detect(text)
        if set == "lang":
            return result.lang
        elif set == "confidence":
            return str(result.confidence)
        else:
            return f"Language: {result.lang}, Confidence: {result.confidence}"
    except Exception as e:
        return f"Помилка: {e}"

def CodeLang(lang: str) -> str:
    lang = lang.lower()
    if lang in LANGUAGES:
        return LANGUAGES[lang]
    for code, name in LANGUAGES.items():
        if name.lower() == lang:
            return code
    return "Помилка: Мову або код не знайдено"

def LanguageList(out: str = "screen", text: str = "") -> str:
    try:
        translator = Translator()
        header = f"{'N':<4} {'Language':<15} {'ISO-639 code':<15} {'Text' if text else ''}"
        lines = [header, "-" * 60]
        
        for i, (code, lang_name) in enumerate(LANGUAGES.items(), 1):
            translated_text = ""
            if text:
                try:
                    translated_text = translator.translate(text, dest=code).text
                except:
                    translated_text = "error"
            lines.append(f"{i:<4} {lang_name.capitalize():<15} {code:<15} {translated_text}")
            
        lines.append("..............................\nOk")
        result_str = "\n".join(lines)

        if out == "file":
            with open("language_list_mod2.txt", "w", encoding="utf-8") as f:
                f.write(result_str)
        else:
            print(result_str)
        return "Ok"
    except Exception as e:
        return f"Помилка: {e}"