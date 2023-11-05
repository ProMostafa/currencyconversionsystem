from datetime import datetime

from django.test import TestCase

from exchangerates.models import Currency
from exchangerates.serializers import ExchangeRateSerializer
from exchangerates.execptions import CurrencyNotSupported


class ExchangeRateSerializerTest(TestCase):
    def setUp(self):
        self.egp_currency = Currency.objects.create(
            code="EGP",
            name="Egyption Pounds",
        )
        self.eur_currency = Currency.objects.create(
            code="EUR",
            name="Euro",
        )

    def test_valid_data(self):
        data = {
            "from_currency": {"code": "EGP", "name": "Egyption Pounds"},
            "to_currency": {"code": "EUR", "name": "Euro"},
            "rate": "1.234",
            "timestamp": datetime.now(),
        }
        serializer = ExchangeRateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_from_currency(self):
        data = {
            "from_currency": {"code": "XCD", "name": "East Caribbean Dollar"},
            "to_currency": {"code": "EUR", "name": "Euro"},
            "rate": "1.234",
            "timestamp": datetime.now(),
        }
        serializer = ExchangeRateSerializer(data=data)
        with self.assertRaises(CurrencyNotSupported):
            serializer.is_valid(raise_exception=True)
        # self.assertFalse(serializer.is_valid())
        # from_currency_errors = serializer.errors.get("non_field_errors", [])
        # self.assertTrue(from_currency_errors)
        # self.assertEqual(
        #     from_currency_errors[0],
        #     "Source currency does not exist in the System Currencies supported.",
        # )

    def test_invalid_to_currency(self):
        data = {
            "from_currency": {"code": "EGP", "name": "Egyption Pounds"},
            "to_currency": {"code": "XCD", "name": "East Caribbean Dollar"},
            "rate": "1.234",
            "timestamp": datetime.now(),
        }
        serializer = ExchangeRateSerializer(data=data)
        with self.assertRaises(CurrencyNotSupported):
            serializer.is_valid(raise_exception=True)
        # to_currency_errors = serializer.errors.get("non_field_errors", [])
        # self.assertTrue(to_currency_errors)
        # self.assertEqual(
        #     to_currency_errors[0],
        #     "Target currency does not exist in the System Currencies supported.",
        # )

    def test_invalid_rate_exchange(self):
        data = {
            "from_currency": {"code": "EGP", "name": "Egyption Pounds"},
            "to_currency": {"code": "EUR", "name": "Euro"},
            "rate": "-1.234",
            "timestamp": datetime.now(),
        }
        serializer = ExchangeRateSerializer(data=data)
        with self.assertRaises(Exception):
            serializer.is_valid(raise_exception=True)

    def test_valid_rate_exchange(self):
        data = {
            "from_currency": {"code": "EGP", "name": "Egyption Pounds"},
            "to_currency": {"code": "EUR", "name": "Euro"},
            "rate": "1.234",
            "timestamp": datetime.now(),
        }
        serializer = ExchangeRateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
