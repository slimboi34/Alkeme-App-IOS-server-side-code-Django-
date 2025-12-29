from django.urls import path
from .views import AlchemyChatView

urlpatterns = [
    path('chat/', AlchemyChatView.as_view(), name='alchemy-chat'),
]
