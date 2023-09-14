import requests
from datetime import datetime


class CurrencyConverter:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = 'https://openexchangerates.org/api/latest.json'

    def convert_currency(self, user_input):
        response = requests.get(self.url, params={'app_id': self.api_key, 'base': 'USD'})

        if response.status_code == 200:
            data = response.json()
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if user_input == 'EXIT':
                return "Good Bye!"

            if user_input in data['rates']:
                rate = data['rates'][user_input]
                return f"{user_input} rate as of {current_datetime}: {rate}"
            else:
                return f"There is no data for currency: {user_input}"
        else:
            return f"An error occurred while receiving data. Status code: {response.status_code}"


def ex_main():
    api_key = '4c4e8fdc5f8b4a1b8c417b629d43d241'
    converter = CurrencyConverter(api_key)

    while True:
        user_input = input("Enter the currency code (e.g. EUR or GBP), or 'EXIT' to exit:").strip().upper()
        result = converter.convert_currency(user_input)
        print(result)
        if result == "Good Bye!":
            break