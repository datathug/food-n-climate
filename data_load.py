from pathlib import Path

import pandas as pd


class PdoRegistry:

    df: pd.DataFrame

    def __init__(self, csv_file: str):

        assert Path(csv_file).is_file(), f"File {csv_file} does not exist"

        self.df = pd.read_csv(csv_file, encoding='utf-8')