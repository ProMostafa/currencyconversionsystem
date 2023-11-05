from django.conf import settings
from .exchange_rate_api import ExchangeRatesAPI
from exchangerates.tests.mocked.exchange_rate_api import MockedExchangeRatesAPI


def get_exchangerates_api():
    if settings.RUNNINGMODE == "development":
        return ExchangeRatesAPI
    return MockedExchangeRatesAPI
