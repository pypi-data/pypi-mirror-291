import requests
import json

def exchange_rate(base=None) -> dict:
    if base is None:
        base = 'USD'
    response = requests.get(f'https://v6.exchangerate-api.com/v6/a60b8b6f52cfb7f8d2dee906/latest/{base}')
    if response.status_code == 200:
        return json.loads(response.text).get('conversion_rates')
    else:
        return {
            'status': response.status_code,
            'messages': 'Base currency is not valid'
        }

if __name__ == "__main__":
   exchange_rate()