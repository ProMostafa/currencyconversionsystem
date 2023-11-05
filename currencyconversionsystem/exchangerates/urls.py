from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CurrencyListView,
    CurrencyDetailView,
    ExchangeRateListView,
    CurrencyConversionViewSet,
)

router = DefaultRouter()
router.register(r"currency-conversions", CurrencyConversionViewSet)

urlpatterns = [
    path(
        "currency/",
        CurrencyListView.as_view(),
        name="currency-list",
    ),
    path(
        "currency/<int:pk>/",
        CurrencyDetailView.as_view(),
        name="currency-detail",
    ),
    path(
        "exchangerate/",
        ExchangeRateListView.as_view(),
        name="exchangerate-list",
    ),
    path("", include(router.urls)),
]
