import os
import json
import google.generativeai as genai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from portfolio.models import Holding
from market.models import Coin

class AlchemyChatView(APIView):
    def post(self, request):
        message = request.data.get('message')
        if not message:
            return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return Response({'error': 'GEMINI_API_KEY not configured'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-flash-latest')
            response = model.generate_content(message)
            return Response({'response': response.text})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PortfolioInsightView(APIView):
    def post(self, request):
        holdings = Holding.objects.all()
        if not holdings.exists():
            return Response({'insight': "Your portfolio is a blank canvas. Start by adding some assets to see the Alchemist's analysis!", 'risk_score': 0, 'suggestions': []})

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return Response({'error': 'GEMINI_API_KEY not configured'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Gather context
        portfolio_summary = []
        for h in holdings:
            coin = Coin.objects.filter(id=h.asset_id).first()
            price = coin.current_price if coin else "Unknown"
            change = coin.price_change_percentage_24h if coin else 0
            portfolio_summary.append(f"- {h.quantity} {h.symbol.upper()} (Price: ${price}, 24h: {change}%)")

        prompt = f"""
        You are 'The Alchemist', a professional crypto portfolio strategist powered by Google Gemini.
        Analyze the following holdings and provide a structured JSON response.
        Enforce a 'clean', institutional-grade tone. Under no circumstances mention non-crypto assets.
        
        JSON format:
        {{
            "insight": "Succinct strategic narrative under 50 words.",
            "risk_score": <int 1-100>,
            "diversification_score": <int 1-100>,
            "yield_forecast": "Succinct 7-day outlook",
            "suggestions": ["Strategic move 1", "Strategic move 2"]
        }}

        Portfolio Data:
        {chr(10).join(portfolio_summary)}
        """

        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-flash-latest', generation_config={"response_mime_type": "application/json"})
            response = model.generate_content(prompt)
            
            clean_text = response.text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text.split("```json")[1].split("```")[0].strip()
            elif clean_text.startswith("```"):
                clean_text = clean_text.split("```")[1].split("```")[0].strip()
                
            return Response(json.loads(clean_text))
        except Exception as e:
            print(f"Portfolio Analysis Error: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MarketBriefingView(APIView):
    def get(self, request):
        top_coins = Coin.objects.all()[:5]
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return Response({'error': 'GEMINI_API_KEY not configured'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        market_data = []
        for c in top_coins:
            market_data.append(f"{c.name} ({c.symbol.upper()}): ${c.current_price}, 24h: {c.price_change_percentage_24h}%")

        prompt = f"""
        You are 'The Alchemist', a professional crypto market analyst via Google Gemini.
        Synthesize the current market narrative based on the provided data.
        Enforce a clean, high-signal tone.
        
        JSON format:
        {{
            "briefing": "Short, powerful one-sentence market pulse.",
            "sentiment": "Bullish" | "Bearish" | "Neutral",
            "fear_greed_index": <int 1-100>
        }}

        Market Data:
        {chr(10).join(market_data)}
        """

        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-flash-latest', generation_config={"response_mime_type": "application/json"})
            response = model.generate_content(prompt)
            
            clean_text = response.text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text.split("```json")[1].split("```")[0].strip()
            elif clean_text.startswith("```"):
                clean_text = clean_text.split("```")[1].split("```")[0].strip()

            return Response(json.loads(clean_text))
        except Exception as e:
            print(f"Market Briefing Error: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AssetInsightView(APIView):
    def post(self, request):
        asset_id = request.data.get('asset_id')
        if not asset_id:
            return Response({'error': 'asset_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        coin = Coin.objects.filter(id=asset_id).first()
        if not coin:
            return Response({'error': 'Asset not found'}, status=status.HTTP_404_NOT_FOUND)

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return Response({'error': 'GEMINI_API_KEY not configured'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        prompt = f"""
        You are 'The Alchemist', a professional crypto analyst via Google Gemini.
        Provide a succinct, insightful 'Take' on the following asset.
        Format your response as a JSON object:
        {{
            "take": "One powerful sentence about the asset's current state/potential.",
            "sentiment": "Bulish" | "Bearish" | "Neutral",
            "key_stat": "A short fact (e.g., 'Approaching All-Time High')"
        }}

        Asset: {coin.name} ({coin.symbol.upper()})
        Price: ${coin.current_price}
        24h Change: {coin.price_change_percentage_24h}%
        Market Cap: ${coin.market_cap}
        """

        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-flash-latest', generation_config={"response_mime_type": "application/json"})
            response = model.generate_content(prompt)
            
            clean_text = response.text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text.split("```json")[1].split("```")[0].strip()
            elif clean_text.startswith("```"):
                clean_text = clean_text.split("```")[1].split("```")[0].strip()

            return Response(json.loads(clean_text))
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
