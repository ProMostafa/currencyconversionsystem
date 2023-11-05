import os
import requests
from abc import ABC, abstractmethod


class ExchangeRatesAPIInterface(ABC):
    # ExchangeRatesAPI Interface
    # Add all method here that can be mocked easily for test
    @abstractmethod
    def fetch_exchange_rates(self, base_currency):
        pass


class ExchangeRatesAPI(ExchangeRatesAPIInterface):
    def fetch_exchange_rates(self, base_currency):
        # Make a real HTTP request to the Exchange Rates API
        exchange_rates_api = os.environ.get("EXCHANGERATEAPI")
        response = requests.get(f"{exchange_rates_api}{base_currency}")
        data = response.json()
        return data
