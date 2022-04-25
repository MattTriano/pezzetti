import json
import os
from typing import Dict, List, Optional
from urllib.request import urlretrieve

import pandas as pd
from pandas.api.types import (
    is_datetime64_any_dtype,
    is_bool_dtype,
    is_bool,
    CategoricalDtype,
)


def get_df_column_details(df: pd.DataFrame) -> pd.DataFrame:
    col_list = list(df.columns)
    n_rows = df.shape[0]
    df_details = pd.DataFrame(
        {
            "feature": [col for col in col_list],
            "unique_vals": [df[col].nunique() for col in col_list],
            "pct_unique": [round(100 * df[col].nunique() / n_rows, 4) for col in col_list],
            "null_vals": [df[col].isnull().sum() for col in col_list],
            "pct_null": [round(100 * df[col].isnull().sum() / n_rows, 4) for col in col_list],
        }
    )
    df_details = df_details.sort_values(by="unique_vals")
    df_details = df_details.reset_index(drop=True)
    return df_details


def get_project_root_dir() -> os.path:
    if "__file__" in globals().keys():
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath("__file__")))
    else:
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(".")))
    # assert ".git" in os.listdir(root_dir)
    return root_dir


def get_global_root_data_dir(
    root_data_dir: os.path = os.path.join(os.path.expanduser("~"), "projects", "data")
) -> os.path:
    os.makedirs(root_data_dir, exist_ok=True)
    return root_data_dir


def read_json(file_path: os.path) -> Dict:
    with open(file_path, "r") as json_file:
        json_data = json.loads(json_file.read())
    return json_data


def extract_csv_from_url(
    file_path: os.path, url: str, force_repull: bool = False, return_df: bool = True
) -> pd.DataFrame:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if not os.path.isfile(file_path) or force_repull:
        urlretrieve(url, file_path)
    if return_df:
        return pd.read_csv(file_path)


def extract_file_from_url(
    file_path: os.path,
    url: str,
    data_format: str,
    force_repull: bool = False,
    return_df: bool = True,
) -> pd.DataFrame:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if not os.path.isfile(file_path) or force_repull:
        urlretrieve(url, file_path)
    if return_df:
        if data_format in ["csv", "zipped_csv"]:
            return pd.read_csv(file_path)
        elif data_format in ["shp", "geojson"]:
            return gpd.read_file(file_path)


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = ["_".join(col.lower().split(" ")) for col in df.columns]
    df.columns = [col.replace("'", "") for col in df.columns]
    return df


def drop_columns(df: pd.DataFrame, columns_to_drop: List) -> pd.DataFrame:
    assert all(
        [col in df.columns for col in columns_to_drop]
    ), "columns_to_drop include missing columns"
    df = df.drop(columns=columns_to_drop)
    return df


def typeset_simple_category_columns(df: pd.DataFrame, category_columns: List[str]) -> pd.DataFrame:
    for category_column in category_columns:
        df[category_column] = df[category_column].astype("category")
    return df


def typeset_ordered_categorical_feature(df: pd.DataFrame, category_column: str) -> pd.DataFrame:
    categories = list(df[category_column].unique())
    categories.sort()
    df[category_column] = series.astype(
        CategoricalDtype(categories=df[category_column], ordered=True)
    )
    return df


def typeset_datetime_column(
    dt_series: pd.Series, dt_format: Optional[str], errors: str = "coerce"
) -> pd.Series:
    dt_series = dt_series.copy()
    if not is_datetime64_any_dtype(dt_series):
        if dt_format is not None:
            try:
                dt_series = pd.to_datetime(dt_series, format=dt_format, errors=errors)
            except:
                dt_series = pd.to_datetime(dt_series, errors=errors)
        else:
            dt_series = pd.to_datetime(dt_series, errors=errors)
    return dt_series


def map_column_to_boolean_values(series: pd.Series, true_values: List[str]) -> pd.DataFrame:
    series = series.copy()
    true_mask = series.isin(true_values)
    if is_bool_dtype(series) or is_bool(series):
        return series
    series.loc[~true_mask] = False
    series.loc[true_mask] = True
    series = series.astype("boolean")
    return series
