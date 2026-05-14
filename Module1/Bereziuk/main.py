import json
import os
from my_module import translate, compare_speeds

FILE_NAME = 'MyData.json'

def request_data_and_exit():
    """Функція для введення даних (Приклад 1)."""
    try:
        v1 = input("Введіть швидкість v1 (км/год): ")
        v2 = input("Введіть швидкість v2 (м/с): ")
        lang = input("Введіть мову інтерфейсу: ")
        
        float(v1.replace(',', '.'))
        float(v2.replace(',', '.'))
        
        data = {
            "v1": v1,
            "v2": v2,
            "lang": lang.strip().lower()
        }
        
        with open(FILE_NAME, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            
        print(f"Дані збережено в файл {FILE_NAME}")
    except ValueError:
        print("Помилка: швидкість має бути числовим значенням. Спробуйте ще раз.")
    
    exit(0)

def main():
    file_is_valid = False
    
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, 'r', encoding='utf-8') as file:
                data = json.load(file)
                v1 = float(str(data['v1']).replace(',', '.'))
                v2 = float(str(data['v2']).replace(',', '.'))
                lang = data.get('lang', 'uk')
                file_is_valid = True
        except (json.JSONDecodeError, KeyError, ValueError):
            file_is_valid = False

    if not file_is_valid:
        request_data_and_exit()

    if lang not in ['uk', 'en']:
        lang = 'uk'

    lang_display = "Українська" if lang == 'uk' else "English"

    results = compare_speeds(v1, v2)

    print(f"{translate('Language', lang)}: {lang_display}")
    
    v1_str = int(v1) if v1.is_integer() else v1
    v2_str = int(v2) if v2.is_integer() else v2
    
    print(f"{translate('Speed', lang)} v1 ({translate('km/h', lang)}): {v1_str}")
    print(f"{translate('Speed', lang)} v2 ({translate('m/s', lang)}): {v2_str}")
    
    v1_converted = round(results['v1_in_ms'], 1)
    v2_converted = round(results['v2_in_kmh'], 1)
    
    v1_conv_str = str(v1_converted).replace('.', ',')
    v2_conv_str = str(int(v2_converted) if v2_converted.is_integer() else v2_converted).replace('.', ',')

    print(f"{translate('Speed', lang)} {v1_str} {translate('km/h', lang)} = {v1_conv_str} {translate('m/s', lang)}")
    print(f"{translate('Speed', lang)} {v2_str} {translate('m/s', lang)} = {v2_conv_str} {translate('km/h', lang)}")
    
    relation_str = translate(results['relation'], lang)
    speed_word_lower = translate('Speed', lang).lower()
    
    print(f"{translate('Speed', lang)} v1={v1_str} {translate('km/h', lang)}, {relation_str} {speed_word_lower} v2={v2_str}{translate('m/s', lang)}")

if __name__ == '__main__':
    main()