import os

surname = os.getenv("SURNAME")

if surname:
    print(f"Знайдено змінну SURNAME. Її значення: {surname}")
else:
    print("Помилка: Змінна SURNAME відсутня або не задана.")