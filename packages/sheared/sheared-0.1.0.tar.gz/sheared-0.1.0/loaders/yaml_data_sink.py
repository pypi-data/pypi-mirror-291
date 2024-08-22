import os

import aiofiles
import pandas as pd
import yaml

from shared.loaders.base import DataSink


class YAMLDataSink(DataSink):
    def __init__(self, output_directory: str):
        if output_directory is not None:
            try:
                self.output_directory = output_directory
                if not os.path.exists(self.output_directory):
                    os.makedirs(self.output_directory)
            except FileExistsError:
                raise FileExistsError(f"Output directory {output_directory} already exists.")

    async def save_data(self, output_file: str = None, data: pd.DataFrame = None) -> None:
        with aiofiles.open(output_file, 'r') as file:
            schema = yaml.safe_load(file)
        return schema

    async def append_data(self, file_path: str = None, data: dict = None):
        pass
