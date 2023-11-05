class CurrencyNotSupported(Exception):
    def __init__(
        self,
        currency_code,
        message="Currency is not supported",
    ):
        self.currency_code = currency_code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.currency_code}: {self.message}"


class ExchageRateNotSupported(Exception):
    def __init__(
        self,
        from_currency,
        to_currency,
        message="Exchage rate is not supported",
    ):
        self.from_currency = from_currency
        self.to_currency = to_currency

        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.from_currency} to {self.to_currency}: {self.message}"


class ConversionAmountNotValid(Exception):
    def __init__(
        self,
        amount,
        message="conversions amount is not valid",
    ):
        self.amount = amount
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.amount}: {self.message}"
