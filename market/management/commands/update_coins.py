import requests
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.base import ContentFile
from market.models import Coin
import time

class Command(BaseCommand):
    help = 'Fetches top 50 coins from CoinGecko and updates the database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--loop',
            action='store_true',
            help='Run the command in an infinite loop with a 60s delay',
        )

    def handle(self, *args, **options):
        loop_mode = options['loop']

        while True:
            self.update_coins()
            
            if not loop_mode:
                break
            
            self.stdout.write(self.style.WARNING("Waiting 60 seconds before next update..."))
            time.sleep(60)

    def update_coins(self):
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 50,
            "page": 1,
            "sparkline": "false",
            "price_change_percentage": "1h,7d" 
        }

        try:
            self.stdout.write("Fetching data from CoinGecko...")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            for item in data:
                try:
                    coin, created = Coin.objects.update_or_create(
                        id=item['id'],
                        defaults={
                            'symbol': item['symbol'],
                            'name': item['name'],
                            'current_price': item['current_price'],
                            'market_cap': item['market_cap'] or 0,
                            'market_cap_rank': item['market_cap_rank'],
                            'price_change_percentage_24h': item['price_change_percentage_24h'] or 0,
                            'price_change_percentage_1h': item.get('price_change_percentage_1h_in_currency') or 0,
                            'price_change_percentage_7d': item.get('price_change_percentage_7d_in_currency') or 0,
                            'total_volume': item['total_volume'] or 0,
                            'circulating_supply': item['circulating_supply'] or 0,
                        }
                    )

                    # Handle Icon Download
                    if not coin.image or not os.path.exists(os.path.join(settings.MEDIA_ROOT, coin.image.name)):
                        image_url = item['image']
                        if image_url:
                            self.stdout.write(f"Downloading icon for {coin.name}...")
                            img_response = requests.get(image_url, timeout=5)
                            if img_response.status_code == 200:
                                filename = f"coins/{coin.id}.png"
                                coin.image.save(filename, ContentFile(img_response.content), save=True)
                                time.sleep(0.5)

                    # Handle Description (Architecture Summary) - Lean fetch
                    # Only fetch if description is missing to avoid rate limits
                    if not coin.description:
                        try:
                            self.stdout.write(f"Fetching details for {coin.name}...")
                            # Rate limit safety: 1.5s delay
                            time.sleep(1.5) 
                            detail_url = f"https://api.coingecko.com/api/v3/coins/{coin.id}"
                            detail_params = {
                                "localization": "false",
                                "tickers": "false",
                                "market_data": "false",
                                "community_data": "false",
                                "developer_data": "false",
                                "sparkline": "false"
                            }
                            detail_resp = requests.get(detail_url, params=detail_params, timeout=10)
                            
                            if detail_resp.status_code == 200:
                                detail_data = detail_resp.json()
                                description = detail_data.get('description', {}).get('en', '')
                                if description:
                                    coin.description = description
                                    coin.save()
                                    self.stdout.write(self.style.SUCCESS(f"Updated description for {coin.name}"))
                            elif detail_resp.status_code == 429:
                                self.stdout.write(self.style.WARNING("Rate limit hit. Cooling down..."))
                                time.sleep(10)
                        except Exception as e:
                             self.stdout.write(self.style.ERROR(f"Error fetching details: {e}"))
                    
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Created {coin.name}"))
                    # else:
                    #     self.stdout.write(f"Updated {coin.name}")
                
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing {item.get('name')}: {e}"))

            self.stdout.write(self.style.SUCCESS('Successfully updated coins'))

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Network error fetching data: {e}"))
