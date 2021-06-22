"""
This module stores code for visualizing the insights from the IPO data.
"""

import numpy as np
import pandas as pd
import plotly.express as px


def plot_histogram_for_column(dataframe: pd.DataFrame,
                              column_header: str,
                              n_bins: int = 20) -> None:
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
                             column_header_y: str) -> None:
    fig = px.scatter(dataframe, x=column_header_x, y=column_header_y)
    fig.show()


def plot_correlation_coefficients(dataframe: pd.DataFrame,
                                  correlate_to_column: str) -> None:
    


def to_signed_float(value):
    value = "".join([char for char in value if char.isdigit() or char == "-"])

    float_value = float(value)

    return float_value


def cast_column_to_signed_float(dataframe: pd.DataFrame, column_header: str) -> pd.DataFrame:
    dataframe[column_header] = dataframe[column_header].apply(to_signed_float)
    return dataframe

