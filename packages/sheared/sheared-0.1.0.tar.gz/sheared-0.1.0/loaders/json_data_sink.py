import json
import os

import aiofiles
import pandas as pd

from shared.loaders.base import DataSink
from shared.config.settings import logger


class JSONDataSink(DataSink):
    def __init__(self, dir_path: str):
        os.makedirs(os.path.dirname(dir_path), exist_ok=True)
        self.dir_path = dir_path

    async def save_data(self, file_path: str, data: dict):
        file_path = os.path.join(self.dir_path, file_path)
        json_data = []

        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            async with aiofiles.open(file_path, 'r') as file:
                try:
                    content = await file.read()
                    json_data = json.loads(content)
                    if not isinstance(json_data, list):
                        json_data = [json_data]
                except json.JSONDecodeError:
                    logger.error(f"Failed to decode JSON from {file_path}")
                    json_data = []

        json_data.append(data)

        async with aiofiles.open(file_path, 'w') as file:
            try:
                await file.write(json.dumps(json_data, indent=4))
                logger.info(f"Data saved to {file_path}")
            except Exception as e:
                logger.error(f"Failed to save data to {file_path}: {e}")

    async def append_data(self, data: dict | list) -> None:
        """ This function is not usable """
        pass

