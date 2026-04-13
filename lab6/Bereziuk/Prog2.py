import urllib.parse
import pyperclip

def main():
    encoded_url = input("Вставте закодоване посилання: ")
    
    decoded_url = urllib.parse.unquote(encoded_url)
    
    print(f"\nДекодоване посилання (I):")
    print(decoded_url)
    
    pyperclip.copy(decoded_url)
    print("\nРезультат скопійовано в буфер обміну!")

if __name__ == "__main__":
    main()