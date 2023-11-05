from django.utils import timezone
from datetime import datetime
from django.conf import settings
from django.db import transaction
from celery import shared_task
from .serializers import ExchangeRateSerializer
from exchangerates.models import Currency
from .execptions import CurrencyNotSupported
from .models import CurrencyConversion, CONVERSION_STATUS
from .utlis import get_exchangerates_api

import logging

logger = logging.getLogger(__name__)


@shared_task
def fetch_exchange_rates():
    # This cause performance issue if number of currencies grow
    # if we design ExchangeRate to serialize this response direct instead of this loop to organize data
    # my be this will be fine if not can think again in design (Just simple design)
    with transaction.atomic():
        ExchangeRatesAPI = get_exchangerates_api()
        api = ExchangeRatesAPI()
        for currency in Currency.objects.all():
            data = api.fetch_exchange_rates(currency.code)
            for exchange_rate in data.get("rates", []):
                try:
                    exchange_object = {
                        "from_currency": {
                            "code": currency.code,
                            "name": currency.name,
                        },
                        "to_currency": exchange_rate.get("currency"),
                        "rate": exchange_rate.get("rate"),
                        "timestamp": datetime.now(),
                    }
                    serializer = ExchangeRateSerializer(
                        data=exchange_object,
                    )
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                except CurrencyNotSupported as e:
                    # logging error here
                    print(e)
                    continue
                except Exception as e:
                    raise e


@shared_task
def update_conversion_status():
    with transaction.atomic():
        permanent_status = CONVERSION_STATUS[0][0]
        temporary_status = CONVERSION_STATUS[1][1]
        # Just for run app in test mode
        if settings.RUNNINGMODE == "test":
            two_days_ago = timezone.now() - timezone.timedelta(minutes=2)
        else:
            two_days_ago = timezone.now() - timezone.timedelta(hours=48)

        temporary_conversions = CurrencyConversion.objects.filter(
            status=temporary_status,
            conversion_date__lte=two_days_ago,
        )
        temporary_conversions.update(status=permanent_status)
