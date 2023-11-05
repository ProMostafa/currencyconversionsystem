from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework import status

from exchangerates.models import Currency, ExchangeRate


class ExchangeRateViewsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="asd",
            password="asd",
        )
        self.from_currency = Currency.objects.create(
            code="EGP",
            name="Egyption Pound",
        )
        self.to_currency = Currency.objects.create(
            code="EUR",
            name="Euro",
        )
        self.exchangerate = ExchangeRate.objects.create(
            from_currency=self.from_currency,
            to_currency=self.to_currency,
            rate="0.03000",
        )
        self.client.force_authenticate(user=self.user)

    def test_exchangerate_list_view(self):
        response = self.client.get(reverse("exchangerate-list"))
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data), 1)
        data = response.data[0]
        self.assertEqual(
            self.exchangerate.from_currency.id,
            data.get("from_currency")["id"],
        )
        self.assertEqual(
            self.exchangerate.to_currency.id,
            data.get("to_currency")["id"],
        )
        self.assertEqual(
            self.exchangerate.rate,
            data.get("rate"),
        )

    def test_currency_create_view(self):
        data = {"from_currency": "1", "to_currency": "2", "rate": "0.22"}
        response = self.client.post(
            reverse("exchangerate-list"),
            data=data,
            format="json",
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )
