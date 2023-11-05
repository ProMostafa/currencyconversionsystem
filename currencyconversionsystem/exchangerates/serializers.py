from decimal import Decimal
from django.utils import timezone

from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Currency, ExchangeRate, CurrencyConversion
from .execptions import (
    CurrencyNotSupported,
    ExchageRateNotSupported,
    ConversionAmountNotValid,
)


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"


class ExchangeRateSerializer(serializers.ModelSerializer):
    from_currency = CurrencySerializer()
    to_currency = CurrencySerializer()
    rate = serializers.DecimalField(
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.DECIMAL_PLACES,
        validators=[MinValueValidator(0)],
    )

    class Meta:
        model = ExchangeRate
        fields = (
            "id",
            "from_currency",
            "to_currency",
            "rate",
            "timestamp",
        )

    def validate(self, data):
        from_currency_data = data.get("from_currency")
        to_currency_data = data.get("to_currency")
        try:
            Currency.objects.get(code=from_currency_data.get("code"))
        except Currency.DoesNotExist:
            raise CurrencyNotSupported(
                from_currency_data.get("code"),
                "Source currency does not exist in the System Currencies supported.",
            )
        try:
            Currency.objects.get(code=to_currency_data.get("code"))
        except Currency.DoesNotExist:
            raise CurrencyNotSupported(
                to_currency_data.get("code"),
                "Target currency does not exist in the System Currencies supported.",
            )
        return data

    def create(self, validated_data):
        from_currency_data = validated_data.pop("from_currency")
        to_currency_data = validated_data.pop("to_currency")
        from_currency = Currency.objects.get(
            code=from_currency_data["code"],
        )
        to_currency = Currency.objects.get(
            code=to_currency_data["code"],
        )
        exchange_rate = ExchangeRate.objects.create(
            from_currency=from_currency, to_currency=to_currency, **validated_data
        )

        return exchange_rate


class CurrencyConversionSerializer(serializers.ModelSerializer):
    from_currency = serializers.CharField(write_only=True)
    to_currency = serializers.CharField(write_only=True)
    exchange_rate = ExchangeRateSerializer(required=False)
    result = serializers.DecimalField(
        decimal_places=settings.DECIMAL_PLACES,
        max_digits=settings.MAX_DIGITS,
        required=False,
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
    )
    conversion_date = serializers.DateTimeField(required=False)

    class Meta:
        model = CurrencyConversion
        fields = (
            "user",
            "amount",
            "conversion_date",
            "exchange_rate",
            "status",
            "result",
            "from_currency",
            "to_currency",
        )

    def validate(self, data):
        from_currency_data = data.get("from_currency")
        to_currency_data = data.get("to_currency")
        amount = Decimal(data.get("amount"))
        if amount <= 0:
            raise ValidationError("Value must be a positive non-zero number.")

        try:
            from_currency = Currency.objects.get(code=from_currency_data)
        except CurrencyNotSupported:
            raise CurrencyNotSupported(from_currency)

        try:
            to_currency = Currency.objects.get(code=to_currency_data)
        except CurrencyNotSupported:
            raise CurrencyNotSupported(to_currency)

        try:
            exsitance = ExchangeRate.objects.filter(
                from_currency=from_currency,
                to_currency=to_currency,
            ).exists()
            if not exsitance:
                raise ExchageRateNotSupported(from_currency, to_currency)
        except ExchageRateNotSupported:
            raise ExchageRateNotSupported(from_currency, to_currency)

        return data

    def create(self, validated_data):
        from_currency_data = validated_data.pop("from_currency")
        to_currency_data = validated_data.pop("to_currency")
        validated_data["user"] = self.context.get("user")
        from_currency = Currency.objects.get(code=from_currency_data)
        to_currency = Currency.objects.get(code=to_currency_data)
        exchange_rate = ExchangeRate.objects.filter(
            from_currency=from_currency,
            to_currency=to_currency,
        ).first()
        validated_data["result"] = (
            Decimal(validated_data.get("amount", 1)) * exchange_rate.rate
        )
        validated_data["conversion_date"] = timezone.now()
        currency_conversion = CurrencyConversion.objects.create(
            exchange_rate=exchange_rate, **validated_data
        )
        return currency_conversion
