"""
API Key configuration for Google Gemini
"""
import os

# Get the API key from environment variable or use the default one

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyDbxotPjzlOxLjT6xb5hy13EhFJQr-E3lA')
