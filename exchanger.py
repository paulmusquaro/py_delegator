import requests
from datetime import datetime


api_key = '4c4e8fdc5f8b4a1b8c417b629d43d241'


url = f'https://openexchangerates.org/api/latest.json'

while True:

    response = requests.post(url, params={'app_id': api_key, 'base': 'USD'})


    if response.status_code == 200:
        data = response.json()


        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        user_input = input(f"Введіть код валюти (наприклад, EUR або GBP), або 'Exit' для виходу: ").strip().upper()


        if user_input == 'EXIT':
            break


        if user_input in data['rates']:
            rate = data['rates'][user_input]
            print(f"Курс {user_input} станом на {current_datetime}: {rate}")
        else:
            print(f"Даних для валюти {user_input} немає в наявності")
    else:
        print(f"Помилка при отриманні даних. Статус код: {response.status_code}")
