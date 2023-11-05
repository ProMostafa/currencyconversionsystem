from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from .validators import validate_positive_nonzero

CONVERSION_STATUS = (
    ("permanent", "permanent"),
    ("temporary", "temporary"),
)


class Currency(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.code


class ExchangeRate(models.Model):
    from_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="from_currency_exchange_rates",
    )
    to_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="to_currencies_exchange_rates",
    )
    rate = models.DecimalField(
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.DECIMAL_PLACES,
        validators=[validate_positive_nonzero],
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = ["from_currency", "to_currency", "timestamp"]
        indexes = [
            models.Index(fields=["from_currency"]),
            models.Index(fields=["to_currency"]),
            models.Index(fields=["from_currency", "to_currency"]),
        ]

    def __str__(self):
        return f"{self.from_currency} to {self.to_currency} on {self.timestamp}"


class CurrencyConversion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.DECIMAL_PLACES,
        validators=[validate_positive_nonzero],
    )
    conversion_date = models.DateTimeField()
    exchange_rate = models.ForeignKey(
        ExchangeRate,
        on_delete=models.CASCADE,
        related_name="exchange_rates",
    )
    status = models.CharField(
        choices=CONVERSION_STATUS,
        max_length=10,
        default=CONVERSION_STATUS[1][1],
    )
    result = models.DecimalField(
        decimal_places=settings.DECIMAL_PLACES,
        max_digits=settings.MAX_DIGITS,
    )

    class Meta:
        ordering = ["-conversion_date"]

    def __str__(self):
        return f"{self.user.username}"
