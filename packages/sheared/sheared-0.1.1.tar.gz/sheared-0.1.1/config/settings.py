# src/config/settings.py
import logging
import os
from dotenv import load_dotenv
import pathlib

# Load environment variables from .env file
load_dotenv()
# Base directory of the project


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Settings:
    # Data directories
    SCRAPERS_PATH = os.getenv("SCRAPERS_PATH")
    BASE_DIR = os.getenv("BASE_DATA_PATH")
    INPUT_DIR = os.path.join(BASE_DIR, 'input')
    OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
    OVERVIEW_DIR = os.path.join(BASE_DIR, 'over_view')
    PROCESSING_DIR = os.path.join(BASE_DIR, 'processing')
    CRAWLED_GMAP_DIR = os.path.join(BASE_DIR, 'output', 'crawled', 'gmap')
    CRAWLED_WEBSITE_DIR = os.path.join(BASE_DIR, 'output', 'crawled', 'website')
    SCRAPED_STATIC_HTML_DIR = os.path.join(BASE_DIR, 'output', 'scraped', 'static_html')
    SCRAPED_HEADLESS_HTML_DIR = os.path.join(BASE_DIR, 'output', 'scraped', 'headless_html')
    SCRAPED_WIKIPEDIA_DIR = os.path.join(BASE_DIR, 'output', 'scraped', 'wikipedia')
    SOCIAL_MEDIA_LINKS_DIR = os.path.join(BASE_DIR, 'output', 'social_media_links')
    API_DATA_DIR = os.path.join(BASE_DIR, 'output', 'api_data')

    # Other settings
    LOG_LEVEL = 'DEBUG'
    DATABASE_URL = 'sqlite:///project_db.sqlite3'

    def __init__(self):
        directories = [
            self.INPUT_DIR,
            self.OUTPUT_DIR,
            self.CRAWLED_WEBSITE_DIR,
            self.CRAWLED_GMAP_DIR,
            self.SCRAPED_STATIC_HTML_DIR,
            self.SCRAPED_HEADLESS_HTML_DIR,
            self.SCRAPED_WIKIPEDIA_DIR,
            self.PROCESSING_DIR,
            self.OVERVIEW_DIR
        ]

        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)

    @staticmethod
    def load_google_api_key():
        return os.getenv("GOOGLE_API_KEY")


settings = Settings()

# print(BASE_DIR)
