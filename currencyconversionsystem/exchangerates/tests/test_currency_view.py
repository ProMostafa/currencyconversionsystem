from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework import status

from exchangerates.models import Currency


class CurrencyViewsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="asd",
            password="asd",
        )
        self.currency = Currency.objects.create(
            code="EGP",
            name="Egyption Pound",
        )
        self.client.force_authenticate(user=self.user)

    def test_currency_list_view(self):
        response = self.client.get(reverse("currency-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Egyption Pound")

    def test_currency_create_view(self):
        data = {"code": "EUR", "name": "Euro"}
        response = self.client.post(
            reverse("currency-list"),
            data=data,
            format="json",
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertTrue(Currency.objects.filter(code="EUR").exists())

    def test_currency_update_view(self):
        data = {"name": "Updates Egyption Pound", "code": "EGP"}
        response = self.client.put(
            reverse("currency-detail", args=[self.currency.id]),
            data=data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.currency.refresh_from_db()
        self.assertEqual(self.currency.name, "Updates Egyption Pound")

    def test_update_nonexistent_currecy(self):
        data = {"name": "Euro", "code": "Euro"}
        response = self.client.put(
            reverse("currency-detail", args=[23]),
            data=data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_currency_delete(self):
        response = self.client.delete(
            reverse("currency-detail", args=[self.currency.id]),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Currency.objects.filter(code="EGP").exists())

    def test_delete_nonexistent_currency(self):
        response = self.client.delete(
            reverse("currency-detail", args=[self.currency.id]),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Currency.objects.filter(code="EGP").exists())
