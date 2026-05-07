import psycopg2
from datetime import date

# Параметри підключення до БД 
DB_PARAMS = {
    "host": "localhost",
    "database": "library_db", 
    "user": "postgres",
    "password": "pass",
    "port": "5432"
}

def print_table(cursor, title):
    """Функція для форматованого виводу результатів у консоль (вимога завдання)."""
    print(f"\n{'='*80}\n{title}\n{'='*80}")
    records = cursor.fetchall()
    if not records:
        print("Немає даних.")
        return
    
    # Отримання заголовків стовпців
    col_names = [desc[0] for desc in cursor.description]
    
    # Визначення максимальної ширини для кожного стовпця
    col_widths = [len(name) for name in col_names]
    for row in records:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))
            
    # Форматування рядка заголовків
    header_row = " | ".join(str(name).ljust(width) for name, width in zip(col_names, col_widths))
    print(header_row)
    print("-" * len(header_row))
    
    # Вивід даних
    for row in records:
        data_row = " | ".join(str(val).ljust(width) for val, width in zip(row, col_widths))
        print(data_row)
    print("-" * len(header_row))

def main():
    try:
        # Встановлення з'єднання
        with psycopg2.connect(**DB_PARAMS) as conn:
            with conn.cursor() as cursor:
                
                # 1. СТВОРЕННЯ ТАБЛИЦЬ З ОБМЕЖЕННЯМИ
                print("Створення таблиць...")
                
                # Видалення існуючих таблиць, якщо вони є (для чистоти експерименту)
                cursor.execute("DROP TABLE IF EXISTS issuances CASCADE;")
                cursor.execute("DROP TABLE IF EXISTS books CASCADE;")
                cursor.execute("DROP TABLE IF EXISTS readers CASCADE;")
                
                # Таблиця: Книги
                cursor.execute("""
                    CREATE TABLE books (
                        inv_num SERIAL PRIMARY KEY,
                        author VARCHAR(100) NOT NULL,
                        title VARCHAR(150) NOT NULL,
                        section VARCHAR(50) CHECK (section IN ('технічна', 'художня', 'економічна')),
                        publish_year INTEGER,
                        pages INTEGER,
                        price NUMERIC(10, 2),
                        kind VARCHAR(50) CHECK (kind IN ('посібник', 'книга', 'періодичне видання')),
                        copies INTEGER,
                        max_days INTEGER
                    );
                """)
                
                # Таблиця: Читачі (маска телефону та обмеження курсу)
                cursor.execute(r"""
                    CREATE TABLE readers (
                        ticket_num SERIAL PRIMARY KEY,
                        surname VARCHAR(50) NOT NULL,
                        name VARCHAR(50) NOT NULL,
                        phone VARCHAR(20) CHECK (phone ~ '^\+380\d{9}$'), -- Маска вводу
                        address VARCHAR(200),
                        course INTEGER CHECK (course >= 1 AND course <= 4), -- Обмеження курсу 1-4
                        group_name VARCHAR(20)
                    );
                """)
                
                # Таблиця: Видача книжок
                cursor.execute("""
                    CREATE TABLE issuances (
                        issue_code SERIAL PRIMARY KEY,
                        issue_date DATE NOT NULL,
                        ticket_num INTEGER REFERENCES readers(ticket_num),
                        inv_num INTEGER REFERENCES books(inv_num)
                    );
                """)
                
                # 2. ЗАПОВНЕННЯ ТАБЛИЦЬ ДАНИМИ
                print("Заповнення таблиць даними...")
                
                # Додавання 14 книг
                books_data = [
                    ('Роберт Мартін', 'Чистий код', 'технічна', 2019, 464, 550.00, 'книга', 5, 30),
                    ('Джордж Оруелл', '1984', 'художня', 1949, 320, 250.00, 'книга', 10, 14),
                    ('Адам Сміт', 'Багатство народів', 'економічна', 2001, 800, 600.00, 'книга', 3, 20),
                    ('Е. Фрімен', 'Паттерни проектування', 'технічна', 2021, 650, 800.00, 'посібник', 2, 45),
                    ('Д. Крейг', 'Економіка для початківців', 'економічна', 2015, 300, 400.00, 'посібник', 4, 30),
                    ('IEEE', 'Журнал комп. наук', 'технічна', 2023, 50, 150.00, 'періодичне видання', 8, 7),
                    ('Рей Бредбері', '451 градус за Фаренгейтом', 'художня', 1953, 256, 200.00, 'книга', 6, 14),
                    ('Економічний вісник', 'Випуск 12', 'економічна', 2023, 60, 100.00, 'періодичне видання', 15, 5),
                    ('Г. Шилдт', 'Java. Керівництво для початківців', 'технічна', 2018, 700, 450.00, 'посібник', 5, 30),
                    ('Стівен Кінг', 'Сяйво', 'художня', 1977, 400, 350.00, 'книга', 4, 14),
                    ('Forbes', 'Тренди 2024', 'економічна', 2024, 80, 250.00, 'періодичне видання', 10, 7),
                    ('Лінус Торвальдс', 'Just for Fun', 'технічна', 2001, 288, 300.00, 'книга', 3, 20),
                    ('Еріх Марія Ремарк', 'Три товариші', 'художня', 1936, 480, 280.00, 'книга', 7, 21),
                    ('Дж. Кейнс', 'Загальна теорія зайнятості', 'економічна', 2007, 350, 450.00, 'книга', 2, 30)
                ]
                cursor.executemany(
                    "INSERT INTO books (author, title, section, publish_year, pages, price, kind, copies, max_days) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    books_data
                )
                
                # Додавання 9 читачів
                readers_data = [
                    ('Коваленко', 'Іван', '+380671234567', 'Київ, Хрещатик 1', 1, 'КН-11'),
                    ('Петренко', 'Олена', '+380509876543', 'Київ, Перемоги 10', 2, 'КН-21'),
                    ('Сидоренко', 'Петро', '+380631112233', 'Бровари, Лісова 5', 3, 'ЕК-31'),
                    ('Григоренко', 'Анна', '+380994445566', 'Київ, Франка 2', 4, 'ПЗ-41'),
                    ('Іванова', 'Марія', '+380677778899', 'Ірпінь, Миру 12', 1, 'ЕК-11'),
                    ('Шевченко', 'Тарас', '+380501239876', 'Київ, Шевченка 15', 2, 'ПЗ-21'),
                    ('Ткаченко', 'Олег', '+380635554433', 'Київ, Науки 40', 3, 'КН-31'),
                    ('Лисенко', 'Дмитро', '+380992223344', 'Київ, Будівельників 8', 4, 'ЕК-41'),
                    ('Мельник', 'Юлія', '+380670001122', 'Вишневе, Європейська 3', 2, 'ПЗ-22')
                ]
                cursor.executemany(
                    "INSERT INTO readers (surname, name, phone, address, course, group_name) VALUES (%s, %s, %s, %s, %s, %s)",
                    readers_data
                )
                
                # Додавання 11 видач
                issuances_data = [
                    (date(2023, 10, 1), 1, 1),
                    (date(2023, 10, 5), 2, 4),
                    (date(2023, 10, 10), 3, 3),
                    (date(2023, 10, 15), 4, 7),
                    (date(2023, 10, 20), 5, 8),
                    (date(2023, 10, 25), 6, 9),
                    (date(2023, 11, 1), 7, 5),
                    (date(2023, 11, 5), 8, 11),
                    (date(2023, 11, 10), 9, 2),
                    (date(2023, 11, 15), 1, 10),
                    (date(2023, 11, 20), 2, 6)
                ]
                cursor.executemany(
                    "INSERT INTO issuances (issue_date, ticket_num, inv_num) VALUES (%s, %s, %s)",
                    issuances_data
                )
                
                # Фіксація змін
                conn.commit()

                # 3. ВИКОНАННЯ ЗАПИТІВ ТА ФОРМАТОВАНИЙ ВИВІД
                
                # Вивід структури та даних таблиць
                cursor.execute("SELECT * FROM books;")
                print_table(cursor, "ТАБЛИЦЯ: Книги (Books)")
                
                cursor.execute("SELECT * FROM readers;")
                print_table(cursor, "ТАБЛИЦЯ: Читачі (Readers)")
                
                cursor.execute("SELECT * FROM issuances;")
                print_table(cursor, "ТАБЛИЦЯ: Видача книжок (Issuances)")

                # Запит 1: Відобразити всі книги, які були видані після 2001 року. Відсортувати назви за алфавітом.
                cursor.execute("""
                    SELECT title, author, publish_year 
                    FROM books 
                    WHERE publish_year > 2001 
                    ORDER BY title ASC;
                """)
                print_table(cursor, "ЗАПИТ 1: Книги, видані після 2001 року (сортування за алфавітом)")

                # Запит 2: Порахувати кількість книг кожного виду (підсумковий запит).
                cursor.execute("""
                    SELECT kind AS "Вид видання", COUNT(*) AS "Кількість унікальних книг", SUM(copies) AS "Загальна кількість примірників"
                    FROM books 
                    GROUP BY kind;
                """)
                print_table(cursor, "ЗАПИТ 2: Кількість книг кожного виду")

                # Запит 3: Відобразити всіх читачів, які брали посібники в бібліотеці. Відсортувати прізвища за алфавітом.
                cursor.execute("""
                    SELECT DISTINCT r.surname, r.name, b.title, b.kind
                    FROM readers r
                    JOIN issuances i ON r.ticket_num = i.ticket_num
                    JOIN books b ON i.inv_num = b.inv_num
                    WHERE b.kind = 'посібник'
                    ORDER BY r.surname ASC;
                """)
                print_table(cursor, "ЗАПИТ 3: Читачі, які брали посібники")

                # Запит 4: Відобразити всі книги за указаним розділом (запит з параметром).
                section_param = 'технічна'
                cursor.execute("SELECT title, author, section FROM books WHERE section = %s;", (section_param,))
                print_table(cursor, f"ЗАПИТ 4: Книги за розділом '{section_param}'")

                # Запит 5: Для кожної книги, яка була видана читачу, порахувати кінцевий термін її повернення в бібліотеку (запит з обчислювальним полем).
                cursor.execute("""
                    SELECT 
                        i.issue_code, 
                        b.title, 
                        i.issue_date AS "Дата видачі", 
                        b.max_days AS "Макс. днів",
                        (i.issue_date + b.max_days) AS "Кінцевий термін повернення"
                    FROM issuances i
                    JOIN books b ON i.inv_num = b.inv_num;
                """)
                print_table(cursor, "ЗАПИТ 5: Кінцевий термін повернення книжок (Обчислювальне поле)")

                # Запит 6: Порахувати кількість посібників, книг та періодичних видань в кожному розділі (перехресний запит).
                cursor.execute("""
                    SELECT 
                        section AS "Розділ",
                        COUNT(CASE WHEN kind = 'посібник' THEN 1 END) AS "Посібники",
                        COUNT(CASE WHEN kind = 'книга' THEN 1 END) AS "Книги",
                        COUNT(CASE WHEN kind = 'періодичне видання' THEN 1 END) AS "Періодичні видання"
                    FROM books
                    GROUP BY section;
                """)
                print_table(cursor, "ЗАПИТ 6: Кількість видів видань по кожному розділу (Перехресний запит)")

    except psycopg2.Error as e:
        print(f"Помилка бази даних: {e}")
    except Exception as e:
        print(f"Сталася помилка: {e}")

if __name__ == "__main__":
    main()