from django.db import models

class Holding(models.Model):
    ASSET_TYPES = [
        ('crypto', 'Cryptocurrency'),
        ('stock', 'Stock'),
    ]
    
    asset_id = models.CharField(max_length=100) # e.g. "bitcoin" or "AAPL"
    asset_type = models.CharField(max_length=10, choices=ASSET_TYPES, default='crypto')
    symbol = models.CharField(max_length=20)   # e.g. "btc" or "AAPL"
    name = models.CharField(max_length=100)    # e.g. "Bitcoin" or "Apple Inc."
    quantity = models.DecimalField(max_digits=30, decimal_places=8)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} {self.symbol} ({self.asset_type})"

class PriceAlert(models.Model):
    CONDITION_CHOICES = [
        ('above', 'Price Above'),
        ('below', 'Price Below'),
    ]
    
    asset_id = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20)
    target_price = models.DecimalField(max_digits=20, decimal_places=8)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='above')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert for {self.symbol} {self.condition} {self.target_price}"
