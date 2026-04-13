import json

def main():
    students = {
        "Шевченко": ["Тарас", "Григорович", 1814],
        "Франко": ["Іван", "Якович", 1856],
        "Леся": ["Українка", "Петрівна", 1871],
        "Коцюбинський": ["Михайло", "Михайлович", 1864],
        "Сковорода": ["Григорій", "Савич", 1722],
        "Грушевський": ["Михайло", "Сергійович", 1866],
        "Стус": ["Василь", "Семенович", 1938],
        "Симоненко": ["Василь", "Андрійович", 1935],
        "Костенко": ["Ліна", "Василівна", 1930],
        "Тичина": ["Павло", "Григорович", 1891]
    }
    
    file_name = 'data.json'
    
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(students, f, ensure_ascii=False, indent=4)
    print(f"Дані збережено у файл {file_name}")
    
    with open(file_name, 'r', encoding='utf-8') as f:
        loaded_data = json.load(f)
    
    print("\n--- Дані з файлу ---")
    for surname, info in loaded_data.items():
        print(f"{surname}: {' '.join(map(str, info))}")

if __name__ == "__main__":
    main()