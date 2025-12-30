from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HoldingViewSet, PriceAlertViewSet

router = DefaultRouter()
router.register(r'holdings', HoldingViewSet)
router.register(r'alerts', PriceAlertViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
