from abc import ABC, abstractmethod

import pandas as pd


class DataSink(ABC):

    @abstractmethod
    def save_data(self, output_file: str, data: pd.DataFrame) -> None:
        pass

    @abstractmethod
    def append_data(self, data: dict | list) -> None:
        pass
