import os
import platform
import requests
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

def main():
    load_dotenv()
    api_key = os.getenv('OPENWEATHER_API_KEY')

    print(f"Операційна система: {platform.system()} {platform.release()}")
    print(f"Версія ядра/системи: {platform.version()}")
    print(f"Python: {platform.python_version()}")

    if not api_key or api_key == "aecef5fd8f3cbe1296eed79607ec1e29":
        print("Увага: API ключ не встановлено як змінна середовища!")
        return

    city_input = input("Введіть назву міста: ")
    url = "https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        'q': city_input,
        'appid': api_key,
        'units': 'metric',
        'lang': 'ua'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status() 
        
        data = response.json()
        
        city_db = data['name']
        
        tz_offset_seconds = data['timezone']
        tz_hours = abs(tz_offset_seconds) // 3600
        tz_minutes = (abs(tz_offset_seconds) % 3600) // 60
        tz_sign = "+" if tz_offset_seconds >= 0 else "-"
        tz_str = f"UTC{tz_sign}{tz_hours:02d}:{tz_minutes:02d}"

        ukraine_tz = timezone(timedelta(hours=3))
        current_time = datetime.now(ukraine_tz)
        time_str = current_time.strftime('%Y-%m-%d %H:%M:%S+03:00')

        sunrise = data['sys']['sunrise']
        sunset = data['sys']['sunset']
        day_length_sec = sunset - sunrise
        dl_hours = day_length_sec // 3600
        dl_minutes = (day_length_sec % 3600) // 60

        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        print(f"Погода у місті {city_input} ({city_db}):")
        print(f"Часова зона: {tz_str}")
        print(f"Дата і час запиту (локальний час): {time_str}")
        print(f"Тривалість дня: {dl_hours}:{dl_minutes:02d} (г:хв)")
        print(f"Опис: {weather_desc}")
        print(f"Температура: {temp} °C (відчувається як {feels_like} °C)")
        print(f"Вологість: {humidity}%")
        print(f"Швидкість вітру: {wind_speed} м/с")

    except requests.exceptions.HTTPError as e:
        print("Помилка: Запит виконався невдало.")
        if response.status_code == 401:
            print("Деталі: Невірний API ключ (401 Unauthorized).")
        elif response.status_code == 404:
            print("Деталі: Місто не знайдено (404 Not Found).")
        else:
            print(f"Деталі: {e}")
    except Exception as e:
        print(f"Непередбачена помилка: {e}")

if __name__ == "__main__":
    main()
    main()
