from pack import module3

print("--- Модуль 3 (deep-translator) ---")
print("Переклад:", module3.TransLate("Добрий день", "uk", "en"))
print("Мова тексту:", module3.LangDetect("Добрий день", "all"))
print("Код мови:", module3.CodeLang("uk"))