from rest_framework import generics
from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework import status

from .models import Currency, CurrencyConversion, ExchangeRate
from .serializers import (
    CurrencySerializer,
    ExchangeRateSerializer,
    CurrencyConversionSerializer,
)


class CurrencyListView(generics.ListCreateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class CurrencyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class ExchangeRateListView(generics.ListCreateAPIView):
    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request):
        raise MethodNotAllowed(request.method)


class CurrencyConversionViewSet(viewsets.ModelViewSet):
    queryset = CurrencyConversion.objects.all()
    serializer_class = CurrencyConversionSerializer

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.filter(user=user)
        return queryset

    @action(detail=False, methods=["POST"])
    def convert(self, request):
        context = {"user": request.user}
        serializer = self.serializer_class(
            data=request.data,
            context=context,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "data": {"contact": serializer.data},
                "message": "Successful Conversion",
            },
            status=status.HTTP_201_CREATED,
        )
