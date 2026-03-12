import json
import os
import re
from pack import module1, module3

def process_file():
    config_file = 'config.json'
    if not os.path.exists(config_file):
        print("Error: Configuration file not found.")
        return

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        file_name = config.get('file_name')
        if not os.path.exists(file_name):
            print(f"Error: Text file '{file_name}' not found.")
            return

        with open(file_name, 'r', encoding='utf-8') as f:
            text = f.read()

        file_size = os.path.getsize(file_name)
        char_count = len(text)
        
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        sentences = [s for s in sentences if s]
        sentence_count = len(sentences)
        
        mod = module1 if config.get('module_name') == "module1" else module3
        lang = mod.LangDetect(text, "lang")

        print(f"The name of the file: {file_name}")
        print(f"File size: {file_size} bite")
        print(f"Number of characters: {char_count}")
        print(f"Number of sentences: {sentence_count}")
        print(f"Text language: {lang}")
        print(f"Text for translation:\n{text}\n")

        limit = config.get('max_sentences', sentence_count)
        text_to_translate = " ".join(sentences[:limit])
        target_lang = config.get('target_language', 'et')

        translated_text = mod.TransLate(text_to_translate, "auto", target_lang)

        if config.get('output') == "screen":
            print(f"Translation language: {target_lang}")
            print(f"Module used: {config.get('module_name')}")
            print(f"Translation:\n{translated_text}")
        elif config.get('output') == "file":
            name, ext = os.path.splitext(file_name)
            new_file = f"{name}_{target_lang}{ext}"
            with open(new_file, 'w', encoding='utf-8') as f:
                f.write(translated_text)
            print("Ok")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    process_file()