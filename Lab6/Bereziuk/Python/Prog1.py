import re

def custom_sort_key(word):
    clean_word = re.sub(r'[^\w]', '', word).lower()
    if not clean_word:
        return (2, word)
    
    first_char = clean_word[0]
    if 'а' <= first_char <= 'щ' or first_char in 'ґєії':
        return (0, clean_word)
    elif 'a' <= first_char <= 'z':
        return (1, clean_word)
    return (2, clean_word)

def main():
    try:
        with open('Python/Task1.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        
        print("--- Вхідний текст ---")
        print(text)
        
        words = re.findall(r'\b\w+\b', text)
        
        sorted_words = sorted(words, key=custom_sort_key)
        
        print("\n--- Відсортовані слова ---")
        print(sorted_words)
        
    except FileNotFoundError:
        print("Помилка: Файл Task1.txt не знайдено.")

if __name__ == "__main__":
    main()