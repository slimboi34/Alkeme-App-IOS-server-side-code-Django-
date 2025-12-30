from django.db import models

class Coin(models.Model):
    id = models.CharField(max_length=100, primary_key=True) # CoinGecko ID (e.g., 'bitcoin')
    symbol = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='coins/', null=True, blank=True)
    current_price = models.DecimalField(max_digits=20, decimal_places=8)
    market_cap = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)
    market_cap_rank = models.IntegerField(null=True, blank=True)
    total_volume = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)
    circulating_supply = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)
    price_change_percentage_1h = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_change_percentage_24h = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_change_percentage_7d = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"

    class Meta:
        ordering = ['market_cap_rank']
