import os

from dotenv import load_dotenv

from sheared.config.settings import logger

# Load environment variables from .env file
load_dotenv()


class SettingsAPIKeyProvider:

    @staticmethod
    def load_google_api_key() -> str:
        try:
            return os.getenv("GOOGLE_API_KEY")
        except AttributeError:
            logger.error(f"Failed to load google API key from settings: {os.getenv('GOOGLE_API_KEY')}")
            raise
