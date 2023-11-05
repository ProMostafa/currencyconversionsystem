from django.contrib import admin
from .models import Currency, ExchangeRate, CurrencyConversion


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("code", "name")


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = (
        "from_currency",
        "to_currency",
        "rate",
        "timestamp",
    )


@admin.register(CurrencyConversion)
class CurrencyConversionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "amount",
        "conversion_date",
        "exchange_rate",
        "status",
        "result",
    )
