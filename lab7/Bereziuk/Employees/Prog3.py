import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def calculate_age(birth_date_str):
    birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
    today = datetime.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def get_age_category(age):
    if age < 18: return "younger_18"
    elif 18 <= age <= 45: return "18-45"
    elif 45 < age <= 70: return "45-70"
    else: return "older_70"

def main():
    csv_file = 'employees.csv'
    
    try:
        df = pd.read_csv(csv_file)
        print("Ok")
    except FileNotFoundError:
        print("Помилка: Файл CSV не знайдено або проблеми при відкритті.")
        return
    except Exception as e:
        print(f"Помилка при читанні файлу CSV: {e}")
        return

    df['Вік'] = df['Дата народження'].apply(calculate_age)
    df['Вікова категорія'] = df['Вік'].apply(get_age_category)

    gender_counts = df['Стать'].value_counts()
    print("\n--- Кількість співробітників за статтю ---")
    print(gender_counts)
    
    plt.figure(figsize=(6, 6))
    gender_counts.plot(kind='pie', autopct='%1.1f%%', colors=['skyblue', 'lightpink'])
    plt.title('Розподіл співробітників за статтю')
    plt.ylabel('')
    plt.show()

    age_counts = df['Вікова категорія'].value_counts().reindex(["younger_18", "18-45", "45-70", "older_70"], fill_value=0)
    print("\n--- Кількість співробітників за віковими категоріями ---")
    print(age_counts)
    
    plt.figure(figsize=(8, 5))
    age_counts.plot(kind='bar', color='coral', edgecolor='black')
    plt.title('Розподіл співробітників за віком')
    plt.xlabel('Вікова категорія')
    plt.ylabel('Кількість')
    plt.xticks(rotation=0)
    plt.show()

    gender_age_counts = df.groupby(['Вікова категорія', 'Стать']).size().unstack(fill_value=0)
    gender_age_counts = gender_age_counts.reindex(["younger_18", "18-45", "45-70", "older_70"])
    
    print("\n--- Розподіл статі за віковими категоріями ---")
    print(gender_age_counts)
    
    gender_age_counts.plot(kind='bar', figsize=(10, 6), color=['skyblue', 'lightpink'], edgecolor='black')
    plt.title('Розподіл статі за віковими категоріями')
    plt.xlabel('Вікова категорія')
    plt.ylabel('Кількість')
    plt.xticks(rotation=0)
    plt.legend(title='Стать')
    plt.show()

if __name__ == "__main__":
    main()