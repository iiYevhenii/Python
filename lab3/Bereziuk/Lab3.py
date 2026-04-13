import asyncio
import time
import re
import os
from googletrans import Translator, LANGUAGES

def CodeLang(lang: str) -> str:
    lang_low = lang.lower()
    if lang_low in LANGUAGES:
        return LANGUAGES[lang_low].capitalize()
    for code, name in LANGUAGES.items():
        if name.lower() == lang_low:
            return code
    return "Error: Language not found"

def LangDetect(txt: str):
    translator = Translator()
    try:
        result = translator.detect(txt)
        conf = result.confidence if result.confidence is not None else 1.0
        return result.lang, conf
    except Exception as e:
        return f"Error: {e}", 0

def TransLate(txt: str, lang: str) -> str:
    translator = Translator()
    target_code = lang if lang.lower() in LANGUAGES else CodeLang(lang)
    if "Error" in target_code: return target_code
    try:
        translation = translator.translate(txt, dest=target_code)
        return translation.text
    except Exception as e:
        return f"Error: {e}"

async def async_translate_sentence(sentence, dest_lang):
    translator = Translator()
    loop = asyncio.get_event_loop()
    try:
        res = await loop.run_in_executor(None, translator.translate, sentence, dest_lang)
        return res.text
    except:
        return "Translation Error"

async def run_async_tasks(text_list, dest_lang):
    tasks = [async_translate_sentence(s, dest_lang) for s in text_list]
    return await asyncio.gather(*tasks)

def main():
    file_name = "Steve_Jobs.txt"
    target_language = "estonian" 
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            full_text = f.read().strip()
            if not full_text:
                print("Error: File is empty.")
                return
    except FileNotFoundError:
        print(f"Error: File {file_name} not found.")
        return

    txt_list = [s.strip() for s in re.split(r'(?<=[.!?])\s+', full_text) if s.strip()]
    target_code = CodeLang(target_language)

    start_sync = time.perf_counter()
    orig_lang_code, confidence = LangDetect(full_text)
    orig_lang_name = CodeLang(orig_lang_code)
    sync_translations = [TransLate(s, target_code) for s in txt_list]
    end_sync = time.perf_counter()

    start_async = time.perf_counter()
    async_translations = asyncio.run(run_async_tasks(txt_list, target_code))
    end_async = time.perf_counter()

    print(f"File name: {file_name}")
    print(f"Symbols: {len(full_text)} | Sentences: {len(txt_list)}")
    print(f"Original language: {orig_lang_name} ({orig_lang_code}), confidence: {confidence}")
    print("-" * 30)
    print("Translation (Synchronous):")
    print(" ".join(sync_translations)) 
    print(f"Time: {end_sync - start_sync:.2f} sec")
    print("-" * 30)
    print("Translation (Asynchronous):")
    print(" ".join(async_translations))
    print(f"Time: {end_async - start_async:.2f} sec")
    
    if (end_async - start_async) < (end_sync - start_sync):
        print(f"\nConclusion: Async is faster by {(end_sync-start_sync)-(end_async-start_async):.2f}s")

if __name__ == "__main__":
    main()