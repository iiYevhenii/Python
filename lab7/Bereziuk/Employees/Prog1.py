import csv
import random
from faker import Faker
from datetime import date

def generate_data():
    fake = Faker(locale='uk_UA')
    
    male_patronymics = [
        "Іванович", "Петрович", "Олександрович", "Сергійович", "Володимирович", 
        "Миколайович", "Вікторович", "Анатолійович", "Михайлович", "Васильович", 
        "Юрійович", "Андрійович", "Богданович", "Тарасович", "Романович", 
        "Дмитрович", "Євгенович", "Григорович", "Степанович", "Максимович", "Павлович"
    ]
    
    female_patronymics = [
        "Іванівна", "Петрівна", "Олександрівна", "Сергіївна", "Володимирівна", 
        "Миколаївна", "Вікторівна", "Анатоліївна", "Михайлівна", "Василівна", 
        "Юріївна", "Андріївна", "Богданівна", "Тарасівна", "Романівна", 
        "Дмитрівна", "Євгенівна", "Григорівна", "Степанівна", "Максимівна", "Павлівна"
    ]

    records = []
    
    start_date = date(1946, 1, 1)
    end_date = date(2011, 12, 31)

    for _ in range(200):
        records.append([
            fake.last_name_female(),
            fake.first_name_female(),
            random.choice(female_patronymics),
            "Жіноча",
            fake.date_between(start_date=start_date, end_date=end_date).strftime("%Y-%m-%d"),
            fake.job(),
            fake.city(),
            fake.address().replace('\n', ', '),
            fake.phone_number(),
            fake.email()
        ])

    for _ in range(300):
        records.append([
            fake.last_name_male(),
            fake.first_name_male(),
            random.choice(male_patronymics),
            "Чоловіча",
            fake.date_between(start_date=start_date, end_date=end_date).strftime("%Y-%m-%d"),
            fake.job(),
            fake.city(),
            fake.address().replace('\n', ', '),
            fake.phone_number(),
            fake.email()
        ])

    random.shuffle(records)
    return records

def main():
    headers = ["Прізвище", "Ім’я", "По батькові", "Стать", "Дата народження", 
               "Посада", "Місто проживання", "Адреса проживання", "Телефон", "Email"]
    
    data = generate_data()
    
    with open('employees.csv', mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)
        
    print("Файл 'employees.csv' успішно створено. Додано 500 записів.")

if __name__ == "__main__":
    main()