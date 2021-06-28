"""
This module stores code for visualizing the insights from the IPO data.
"""

from typing import List

import numpy as np
import pandas as pd
import plotly.express as px


def plot_histogram_for_column(dataframe: pd.DataFrame,
                              column_header: str,
                              n_bins: int = 20):
    """
    Plots a histogram for the given column
    :param dataframe: IPO dataframe
    :param column_header: column header label
    :param n_bins: number of bins to use
    """
    fig = px.histogram(dataframe, x=column_header, title=column_header, nbins=n_bins)
    fig.show()


def plot_scatter_for_columns(dataframe: pd.DataFrame,
                             column_header_x: str,
                             column_header_y: str):
    """
    Plots a scatter plot using two specified columns in a dataframe.
    :param dataframe: IPO dataframe
    :param column_header_x: header label for column to use as X axis
    :param column_header_y: header label for column to use as Y axis
    """
    fig = px.scatter(dataframe, x=column_header_x, y=column_header_y)
    fig.show()


def plot_box_for_columns(dataframe: pd.DataFrame,
                         column_header_x: str,
                         column_header_y: str):
    """
    Plots a box plot using two specified columns in a dataframe.
    :param dataframe: IPO dataframe
    :param column_header_x: header label for column to use as X axis
    :param column_header_y: header label for column to use as Y axis
    """
    fig = px.box(dataframe, x=column_header_x, y=column_header_y)
    fig.show()


def plot_correlation_coefficients(dataframe: pd.DataFrame,
                                  correlate_to_column: str,
                                  columns_to_check: List[str],
                                  binary_correlation: bool):
    corr_coefs = []
    for column_label in columns_to_check:
        base_column = dataframe[correlate_to_column]

        if binary_correlation:
            binary_column = dataframe[correlate_to_column]
            binary_column[binary_column > 0] = 1
            binary_column[binary_column < 0] = -1
            base_column = binary_column

        corr_coef = np.corrcoef(base_column, dataframe[column_label])[0, 1]
        corr_coefs.append(corr_coef)

    fig = px.scatter(x=columns_to_check, y=corr_coefs, title=f"Correlation coefficient to column {correlate_to_column}")
    fig.show()


def to_signed_float(value: str) -> float:
    """
    Converts a value in string format to signed float
    :param value: string that contains a value
    :return: value converted to signed float
    """
    # Removes all non digit chars except for - sign
    value = "".join([char for char in value if char.isdigit() or char in ["-", "."]])
    float_value = float(value)
    return float_value


def cast_column_to_signed_float(dataframe: pd.DataFrame, column_header: str) -> pd.DataFrame:
    """
    Casts a column in a dataframe to signed float format,
    :param dataframe: IPO dataframe
    :param column_header: header label for column to cast to float
    :return: dataframe with column modified.
    """

    # TODO: fix warning here
    dataframe[column_header] = dataframe[column_header].apply(to_signed_float)
    return dataframe

