from pack import module1

print("--- Модуль 1 (googletrans 4.0.2) ---")
print("Переклад:", module1.TransLate("Добрий день", "uk", "en"))
print("Мова тексту:", module1.LangDetect("Добрий день", "all"))
print("Код мови:", module1.CodeLang("uk"))