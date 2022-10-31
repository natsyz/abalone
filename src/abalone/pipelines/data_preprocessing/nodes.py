"""
This is a boilerplate pipeline 'data_preprocessing'
generated using Kedro 0.18.3
"""
from typing import List
import pandas as pd

def drop_dataset(dataset: pd.DataFrame, columns: List) -> pd.DataFrame:
    """Drop kolom-kolom pada dataset.

    Keyword arguments:
    dataset -- Dataset yang kolomnya akan di-drop
    columns -- List kolom pada dataset yang akan di-drop
    """
    # drop data duplikat
    dataset.drop_duplicates(inplace=True, ignore_index=True)
    # drop atribut yang dianggap tidak penting
    dataset.drop(columns=columns, axis=1, inplace=True)
    
    return dataset

def preprocessing(dataset: pd.DataFrame) -> pd.DataFrame:
    """Melakukan pemrosesan data [dropna].

    Keyword arguments:
    dataset -- Dataset yang akan di-preprocessing
    """
    # Hapus baris yang terdapat nilai null
    dataset.dropna(inplace=True)

    return dataset