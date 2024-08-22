import os

import aiofiles
import pandas as pd

from sheared.loaders.base import DataSink
from sheared.config.settings import logger


class CSVDataSink(DataSink):
    def __init__(self, output_directory: str):
        if output_directory is not None:
            try:
                self.output_directory = output_directory
                if not os.path.exists(self.output_directory):
                    os.makedirs(self.output_directory)
            except FileExistsError:
                raise FileExistsError(f"Output directory {output_directory} already exists.")

    async def save_data(self, output_file: str = None, data: pd.DataFrame = None) -> None:
        if output_file is not None and data is not None:
            output_path = os.path.join(self.output_directory, output_file)
            if ~isinstance(data, pd.DataFrame):
                data = pd.DataFrame(data)
            data.to_csv(output_path, index=False)
            logger.info(f"Data saved to {output_path}")
        else:
            raise ValueError("File name and Data name should not be None")

    async def append_data(self, file_path: str = None, data: dict = None):
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary.")
        if data is not None:
            file_path = file_path if file_path.endswith('.csv') else f'{file_path}.csv'
            full_path = f'{self.output_directory}/{file_path}'

            async with aiofiles.open(full_path, 'a') as file:
                await file.write(str(data) + '\n')
