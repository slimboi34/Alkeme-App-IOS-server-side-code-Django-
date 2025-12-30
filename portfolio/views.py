from rest_framework import viewsets
from .models import Holding, PriceAlert
from .serializers import HoldingSerializer, PriceAlertSerializer

class HoldingViewSet(viewsets.ModelViewSet):
    queryset = Holding.objects.all()
    serializer_class = HoldingSerializer

class PriceAlertViewSet(viewsets.ModelViewSet):
    queryset = PriceAlert.objects.all()
    serializer_class = PriceAlertSerializer
