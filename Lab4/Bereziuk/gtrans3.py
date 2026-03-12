from pack import module2

print("--- Module 2 (googletrans 3.1.0a0) ---")
print("Translation:", module2.TransLate("Добрий день", "uk", "et"))
print("Text language:", module2.LangDetect("Добрий день", "all"))
print("Code language:", module2.CodeLang("uk"))
module2.LanguageList("screen", "Добрий день")