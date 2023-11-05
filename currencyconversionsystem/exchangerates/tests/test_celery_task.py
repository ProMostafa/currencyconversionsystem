from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from django.db.models import Q
from django.contrib.auth.models import User
from django.test import TestCase
from exchangerates.models import (
    Currency,
    ExchangeRate,
    CurrencyConversion,
    CONVERSION_STATUS,
)
from exchangerates.tasks import fetch_exchange_rates, update_conversion_status


class FetchExchangeRatesTest(TestCase):
    def test_fetch_exchange_rates_that_supported(self):
        settings.RUNNINGMODE = ""
        egp_currency = Currency.objects.create(
            code="EGP",
            name="Egyptian pound",
        )
        eur_currency = Currency.objects.create(
            code="EUR",
            name="Euro",
        )
        fetch_exchange_rates()
        egp_exchanges_rates = ExchangeRate.objects.filter(
            from_currency=egp_currency,
        )

        self.assertEqual(len(egp_exchanges_rates), 1)
        eur_exchanges_rates = ExchangeRate.objects.filter(
            from_currency=eur_currency,
        )
        self.assertEqual(len(eur_exchanges_rates), 1)
        not_supported_currency = ExchangeRate.objects.filter(
            Q(from_currency__code="USD") | Q(to_currency__code="USD")
        )
        self.assertEqual(len(not_supported_currency), 0)


class UpdateConvertionStatusTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="asd",
            password="asd",
        )
        egp_currency = Currency.objects.create(
            code="EGP",
            name="Egyption Pound",
        )
        usd_currency = Currency.objects.create(
            code="USD",
            name="USD",
        )
        self.exchange_rate = ExchangeRate.objects.create(
            from_currency=egp_currency,
            to_currency=usd_currency,
            rate=0.033,
        )
        self.permanent_status = CONVERSION_STATUS[0][0]
        self.temporary_status = CONVERSION_STATUS[1][1]
        settings.RUNNINGMODE = ""

    def test_update_convertion_status_to_permanent_after_48h(self):
        egp_to_usd = CurrencyConversion.objects.create(
            user=self.user,
            amount=20,
            exchange_rate=self.exchange_rate,
            result=1000,
            conversion_date=timezone.now() - timedelta(hours=49),
        )
        egp_to_usd.refresh_from_db()
        self.assertEqual(
            egp_to_usd.status,
            self.temporary_status,
        )
        update_conversion_status()
        egp_to_usd.refresh_from_db()
        self.assertEqual(
            egp_to_usd.status,
            self.permanent_status,
        )

    def test_convertions_that_less_that_48h_not_changed(self):
        egp_to_usd1 = CurrencyConversion.objects.create(
            user=self.user,
            amount=20,
            exchange_rate=self.exchange_rate,
            result=1000,
            conversion_date=timezone.now() - timedelta(hours=49),
        )
        egp_to_usd2 = CurrencyConversion.objects.create(
            user=self.user,
            amount=20,
            exchange_rate=self.exchange_rate,
            result=1000,
            conversion_date=timezone.now() - timedelta(hours=46),
        )
        update_conversion_status()
        egp_to_usd1.refresh_from_db()
        egp_to_usd2.refresh_from_db()
        self.assertEqual(
            egp_to_usd1.status,
            self.permanent_status,
        )
        self.assertEqual(
            egp_to_usd2.status,
            self.temporary_status,
        )
