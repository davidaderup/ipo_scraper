"""
This is a script that extracts data from the IPO Guiden website into a pandas Dataframe and saves it as a excel sheet.
"""

import argparse

import pandas as pd

from ipo_scraper import web_scraper
import ipo_scraper.dataframe_keys as dfk


def extract_ipo_data_to_dataframe(output_path: str):
    """
    Extracts IPO data to a pandas Dataframe and saves it to specified path as a csv file
    """
    ipo_guiden_url = "https://www.affarsvarlden.se/ipo-guiden/screener"
    driver = web_scraper.get_chrome_driver_for_url(url=ipo_guiden_url)
    # Removes pop up
    import time
    time.sleep(2)
    web_scraper.remove_ad(chrome_driver=driver)
    # Scroll to get rid of dynamic ad at top of webpage
    driver.execute_script(f"window.scrollTo(0, {1080})")
    web_scraper.toggle_all_keys_to_true(chrome_driver=driver, is_default_layout=True)
    web_scraper.show_all_ipos(chrome_driver=driver)
    table = web_scraper.get_ipo_table(driver=driver, id="datatable_overview")
    header_labels = web_scraper.get_ipo_headers(table=table)
    flag_column_ind = header_labels.index(dfk.N_FLAGS)
    flag_dict = web_scraper.get_flag_dict(chrome_driver=driver, table=table, flag_column_ind=flag_column_ind)
    df_dict = web_scraper.extract_table_body_to_dict(table=table,
                                                     header_labels=header_labels)
    df_dict.update(flag_dict)
    dataframe = pd.DataFrame(data=df_dict)
    print("Sneak peek of the goodies:")
    print(dataframe)
    print(f"Saving Dataframe to {output_path}")
    dataframe.to_csv(output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extracts IPO data to a pandas Dataframe and saves it "
                                                 "to specified path as a csv file")
    parser.add_argument("-o",
                        "--output-path",
                        type=str,
                        help="Path where to save the dataframe csv file")
    args = parser.parse_args()
    extract_ipo_data_to_dataframe(output_path=args.output_path)
