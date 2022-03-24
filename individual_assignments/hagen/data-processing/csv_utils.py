import pandas as pd


def load_csv(csv_file_path, delimiter=',', index_col=None, low_memory=True):
    return pd.read_csv(csv_file_path,
                       delimiter=delimiter,
                       index_col=index_col,
                       low_memory=low_memory)


def save_csv(df, csv_file_path, index=False):
    df.to_csv(csv_file_path, index=index)
