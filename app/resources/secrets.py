import os
from dotenv import load_dotenv

load_dotenv()

if os.environ.get('API_AUTH_SECRET'):
    API_KEY = os.environ.get('API_AUTH_SECRET')
else:
    API_KEY = "12345678901234567890"
