# Create class for CoinGecko API

import requests

class CoinGeckoAPI:
    def __init__(self):
        self.api_url = "https://api.coingecko.com/api/v3/"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

    def get_price(self, coin_id, vs_currency):
        params = {
            'ids': coin_id,
            'vs_currencies': vs_currency,
        }
        response = requests.get(self.api_url + 'simple/price', params=params, headers=self.headers)
        return response.json()['bitcoin'][vs_currency]