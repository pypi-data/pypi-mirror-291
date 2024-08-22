# src/core/utils.py

import os
import logging
from pathlib import Path
from urllib.parse import urlparse
import pandas as pd

from sheared.config.settings import settings


def setup_logging(log_level: str = 'DEBUG'):
    """
    Setup logging configuration.

    Parameters
    ----------
    log_level : str, optional
        The logging level (default is 'DEBUG').
    """
    logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


async def create_directory(directory: str):
    """
    Create a directory if it doesn't exist.

    Parameters
    ----------
    directory : str
        The path of the directory to be created.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


async def get_domain(url: str) -> str:
    """
    Extract the domain from a given URL.

    Parameters
    ----------
    url : str
        The URL from which to extract the domain.

    Returns
    -------
    str
        The extracted domain.
    """
    parsed_url = urlparse(url)
    hostname = parsed_url.netloc or parsed_url.path.split('/')[0]
    hostname = hostname.split(':')[0]  # Remove port number if present
    hostname = hostname[4:] if hostname.startswith('www.') else hostname
    parts = hostname.split('.')
    return '.'.join(parts[-2:]) if len(parts) > 2 else hostname


def append_crawled_url(url:str, file_path=f'{settings.PROCESSING_DIR}\\crawled_urls.csv'):
    """
    Appends a given URL to a CSV file, creating the file if it doesn't exist,
    and ensuring that it does not delete old URLs.

    Args:
    url (str): The URL to be saved.
    file_path (str): Path to the CSV file where URLs are saved. Default is 'seen_urls.csv'.
    """
    # Create a DataFrame for the new URL
    df_new_url = pd.DataFrame([url], columns=['urls'])

    # Check if the CSV file exists
    if Path(file_path).exists():
        # Append the new URL to the existing CSV without reading the entire file into memory
        df_new_url.to_csv(file_path, mode='a', header=False, index=False)
    else:
        # Create a new CSV file with a header
        df_new_url.to_csv(file_path, mode='w', header=True, index=False)
