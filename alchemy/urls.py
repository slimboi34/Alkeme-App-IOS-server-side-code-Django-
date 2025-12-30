from django.urls import path
from .views import AlchemyChatView, PortfolioInsightView, MarketBriefingView, AssetInsightView

urlpatterns = [
    path('chat/', AlchemyChatView.as_view(), name='alchemy-chat'),
    path('portfolio-insight/', PortfolioInsightView.as_view(), name='portfolio-insight'),
    path('market-briefing/', MarketBriefingView.as_view(), name='market-briefing'),
    path('asset-insight/', AssetInsightView.as_view(), name='asset-insight'),
]
