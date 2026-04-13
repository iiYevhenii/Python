from deep_translator import GoogleTranslator
from langdetect import detect, detect_langs

def TransLate(text: str, scr: str, dest: str) -> str:
    try:
        translated = GoogleTranslator(source=scr, target=dest).translate(text)
        return translated
    except Exception as e:
        return f"Помилка: {e}"

def LangDetect(text: str, set: str = "all") -> str:
    try:
        if set == "lang":
            return detect(text)
        elif set == "confidence":
            langs = detect_langs(text)
            return str(langs[0].prob)
        else:
            langs = detect_langs(text)
            return f"Language: {langs[0].lang}, Confidence: {langs[0].prob}"
    except Exception as e:
        return f"Помилка: {e}"

def CodeLang(lang: str) -> str:
    try:
        langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)
        lang = lang.lower()
        if lang in langs_dict.values():
            for name, code in langs_dict.items():
                if code == lang:
                    return name
        elif lang in langs_dict:
            return langs_dict[lang]
        return "Помилка: Мову або код не знайдено"
    except Exception as e:
        return f"Помилка: {e}"

def LanguageList(out: str = "screen", text: str = "") -> str:
    try:
        langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)
        header = f"{'N':<4} {'Language':<15} {'ISO-639 code':<15} {'Text' if text else ''}"
        lines = [header, "-" * 60]
        
        for i, (lang_name, code) in enumerate(langs_dict.items(), 1):
            translated_text = ""
            if text:
                try:
                    translated_text = GoogleTranslator(source='auto', target=code).translate(text)
                except:
                    translated_text = "error"
            lines.append(f"{i:<4} {lang_name.capitalize():<15} {code:<15} {translated_text}")
            
        lines.append("..............................\nOk")
        result_str = "\n".join(lines)

        if out == "file":
            with open("language_list_mod3.txt", "w", encoding="utf-8") as f:
                f.write(result_str)
        else:
            print(result_str)
        return "Ok"
    except Exception as e:
        return f"Помилка: {e}"