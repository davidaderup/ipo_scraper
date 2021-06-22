"""
Script for plotting the latest and greatest findings from the IPO data.
"""

from pathlib import Path

import pandas as pd
import plotly.express as px

import ipo_scraper.visualization as viz

csv_file_path = Path(r"C:\ipo\test.csv")

dataframe = pd.read_csv(csv_file_path)

print(dataframe)

finished_ipos_dataframe = dataframe[dataframe["Utveckling"] != "-"]

print(finished_ipos_dataframe)

viz.cast_column_to_signed_float(dataframe=finished_ipos_dataframe, column_header="Flaggor")
viz.cast_column_to_signed_float(dataframe=finished_ipos_dataframe, column_header="Erbjudande")
viz.cast_column_to_signed_float(dataframe=finished_ipos_dataframe, column_header="Utveckling")

viz.plot_histogram_for_column(dataframe=finished_ipos_dataframe, column_header="Flaggor")
viz.plot_histogram_for_column(dataframe=finished_ipos_dataframe, column_header="Erbjudande")
viz.plot_histogram_for_column(dataframe=finished_ipos_dataframe, column_header="Utveckling", n_bins=100)

viz.plot_scatter_for_columns(dataframe=finished_ipos_dataframe, column_header_x="Flaggor", column_header_y="Utveckling")


