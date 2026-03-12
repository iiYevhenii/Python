from pack import module3

print("--- Module 3 (deep-translator) ---")
print("Translation:", module3.TransLate("Добрий день", "uk", "et"))
print("Text language:", module3.LangDetect("Добрий день", "all"))
print("Code language:", module3.CodeLang("uk"))
module3.LanguageList("screen", "Добрий день")