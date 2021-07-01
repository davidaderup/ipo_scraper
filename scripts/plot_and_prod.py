"""
Script for plotting the latest and greatest findings from the IPO data.
"""

from pathlib import Path

import pandas as pd

import ipo_scraper.visualization as viz

import ipo_scraper.dataframe_keys as dfk

csv_file_path = Path(r"C:\ipo\big_boy.csv")

dataframe = pd.read_csv(csv_file_path)

print(dataframe)


# Filter out missing entries
finished_ipos_dataframe = dataframe[dataframe[dfk.OUTCOME_TO_DATE] != "-"]
finished_ipos_dataframe = finished_ipos_dataframe[finished_ipos_dataframe[dfk.OUTCOME_FIRST_DAY] != "-"]
finished_ipos_dataframe = finished_ipos_dataframe[finished_ipos_dataframe[dfk.KEY_PERSON_STAKE] != "Uppgift saknas"]

print(finished_ipos_dataframe)

columns_to_cast = [dfk.N_FLAGS,
                   dfk.TOTAL_OFFER,
                   dfk.OUTCOME_TO_DATE,
                   dfk.OUTCOME_FIRST_DAY,
                   dfk.NEW_ISSUE_PART,
                   dfk.SECURED_STAKE,
                   dfk.KEY_PERSON_STAKE,
                   dfk.STOCK_PRICE_OFFER]
for column_header in columns_to_cast:
    viz.cast_column_to_signed_float(dataframe=finished_ipos_dataframe, column_header=column_header)

flags = [flag for ind, flag in enumerate(finished_ipos_dataframe.keys()) if ind >= 25]

viz.plot_correlation_coefficients(dataframe=finished_ipos_dataframe,
                                  correlate_to_column=dfk.OUTCOME_TO_DATE,
                                  columns_to_check=flags,
                                  binary_correlation=False)

# viz.plot_histogram_for_column(dataframe=finished_ipos_dataframe, column_header=dfk.N_FLAGS)
# viz.plot_histogram_for_column(dataframe=finished_ipos_dataframe, column_header=dfk.TOTAL_OFFER)
# viz.plot_histogram_for_column(dataframe=finished_ipos_dataframe, column_header=dfk.OUTCOME_TO_DATE, n_bins=100)


# viz.plot_scatter_for_columns(dataframe=finished_ipos_dataframe, column_header_x=dfk.STOCK_PRICE_OFFER, column_header_y=dfk.OUTCOME_FIRST_DAY)
# viz.plot_scatter_for_columns(dataframe=finished_ipos_dataframe, column_header_x=dfk.STOCK_PRICE_OFFER, column_header_y=dfk.OUTCOME_TO_DATE)



# viz.plot_box_for_columns(dataframe=finished_ipos_dataframe, column_header_x=dfk.N_FLAGS, column_header_y=dfk.OUTCOME_TO_DATE)
# viz.plot_scatter_for_columns(dataframe=finished_ipos_dataframe, column_header_x=dfk.N_FLAGS, column_header_y=dfk.OUTCOME_FIRST_DAY)
#
#
# viz.plot_correlation_coefficients(dataframe=finished_ipos_dataframe,
#                                   correlate_to_column=dfk.N_FLAGS,
#                                   columns_to_check=[dfk.OUTCOME_TO_DATE, dfk.OUTCOME_FIRST_DAY],
#                                   binary_correlation=False)

