import os
import google.generativeai as genai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class AlchemyChatView(APIView):
    def post(self, request):
        message = request.data.get('message')
        if not message:
            return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
             # For development purposes, if no key is found, return a mock response or specific error
             return Response({'error': 'GEMINI_API_KEY not configured in environment variables'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(message)
            return Response({'response': response.text})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
