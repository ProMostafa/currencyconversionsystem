from datetime import datetime

from exchangerates.exchange_rate_api import ExchangeRatesAPIInterface
from .utils import generate_random_rate


class MockedExchangeRatesAPI(ExchangeRatesAPIInterface):
    def fetch_exchange_rates(self, base_currency):
        # Provide mock data for testing
        if base_currency == "EGP":
            return {
                "timestamp": datetime.now(),
                "base": "EGP",
                "rates": [
                    {
                        "currency": {"code": "USD", "name": "United States dollar"},
                        "rate": generate_random_rate(),
                    },
                    {
                        "currency": {"code": "EUR", "name": "EUR"},
                        "rate": generate_random_rate(),
                    },
                ],
            }
        elif base_currency == "EUR":
            return {
                "timestamp": datetime.now(),
                "base": "EUR",
                "rates": [
                    {
                        "currency": {"code": "USD", "name": "United States dollar"},
                        "rate": generate_random_rate(),
                    },
                    {
                        "currency": {"code": "EGP", "name": "Egyptian pound"},
                        "rate": generate_random_rate(),
                    },
                ],
            }
        elif base_currency == "USD":
            return {
                "timestamp": datetime.now(),
                "base": "USD",
                "rates": [
                    {
                        "currency": {"code": "EGP", "name": "Egyptian pound"},
                        "rate": generate_random_rate(),
                    },
                    {
                        "currency": {"code": "EUR", "name": "EUR"},
                        "rate": generate_random_rate(),
                    },
                ],
            }
