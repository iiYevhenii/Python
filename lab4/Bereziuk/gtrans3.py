from pack import module2

print("--- Модуль 2 (googletrans 3.1.0a0) ---")
print("Переклад:", module2.TransLate("Добрий день", "uk", "en"))
print("Мова тексту:", module2.LangDetect("Добрий день", "all"))
print("Код мови:", module2.CodeLang("uk"))