from pathlib import Path

from pandas import DataFrame, read_csv


def _retrieve_existing_data(file_path: Path) -> DataFrame:
    if file_path.exists():
        data_df = read_csv(file_path)
    else:
        data_df = DataFrame()
    return data_df
