from pack import module1

print("--- Module 1 (googletrans 4.0.2) ---")
print("Translation:", module1.TransLate("Добрий день", "uk", "et"))
print("Text language:", module1.LangDetect("Добрий день", "all"))
print("Code language:", module1.CodeLang("uk"))
module1.LanguageList("screen", "Добрий день")