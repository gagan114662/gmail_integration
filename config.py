import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration management for Gmail Signal Integration"""

    # Gmail API Configuration
    GMAIL_CLIENT_ID = os.getenv('GMAIL_CLIENT_ID')
    GMAIL_CLIENT_SECRET = os.getenv('GMAIL_CLIENT_SECRET')
    GMAIL_REFRESH_TOKEN = os.getenv('GMAIL_REFRESH_TOKEN')
    GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    # Pub/Sub Configuration
    PUBSUB_TOPIC_NAME = os.getenv('PUBSUB_TOPIC_NAME')

    # Mathematricks API Configuration
    MATHEMATRICKS_API_URL = os.getenv('MATHEMATRICKS_API_URL', 'https://mathematricks.fund/api/signals')
    MATHEMATRICKS_PASSPHRASE = os.getenv('MATHEMATRICKS_PASSPHRASE')

    # Strategy Configuration
    STRATEGY_NAME = os.getenv('STRATEGY_NAME', 'Gmail_Signal_Integration')

    # Signal Detection Configuration
    SIGNAL_IDENTIFIER = os.getenv('SIGNAL_IDENTIFIER', 'SIGNAL')

    # Flask Configuration
    FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))

    @classmethod
    def validate(cls):
        """Validate that all required configuration is present"""
        required_vars = [
            'GMAIL_CLIENT_ID',
            'GMAIL_CLIENT_SECRET',
            'MATHEMATRICKS_PASSPHRASE'
        ]

        missing = []
        for var in required_vars:
            if not getattr(cls, var):
                missing.append(var)

        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")

        return True
