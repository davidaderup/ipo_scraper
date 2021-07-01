"""
This module contains most code related to scraping the content of IPO guiden
"""

from typing import List, Dict
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import bs4
import numpy as np

import ipo_scraper.dataframe_keys as dfk

def get_chrome_driver_for_url(url: str) -> webdriver.Chrome:
    """
    Gets a Chrome WebDriver object for a specified URL.
    :param url: URL to a website
    :return: Chrome WebDriver connected to the URL
    """
    driver = webdriver.Chrome()
    driver.get(url=url)
    return driver


def remove_ad(chrome_driver: webdriver.Chrome):
    """
    Closes the popup ad that appears when you first open the IPO guiden website
    :param chrome_driver: Selenium Chrome WebDriver object that navigates the website
    """
    # this xpath is hardcoded to the button with text "STÄNG X" for the ad that I encountered when making this,
    # It is a google generated ad so it might be subject to change.
    xpath_to_close_ad = "/html/body/div[8]/div/div/button"
    click_item_at_xpath(chrome_driver=chrome_driver, xpath=xpath_to_close_ad)


def show_all_ipos(chrome_driver: webdriver.Chrome):
    """
    Shows all IPOs on one page of the IPO guiden website.
    :param chrome_driver: Selenium Chrome WebDriver object that navigates the website
    """
    # This is the path to the option which lists all IPOs in the dropdown list at the bottom of the page.
    xpath_to_list_all_ipos = "/html/body/main/section[2]/div[2]/div[3]/label/select/option[6]"
    click_item_at_xpath(chrome_driver=chrome_driver, xpath=xpath_to_list_all_ipos)


def click_item_at_xpath(chrome_driver: webdriver.Chrome, xpath: str):
    """
    Clicks an item at a given xpath
    :param chrome_driver: Selenium Chrome WebDriver object that navigates the website
    :param xpath: path to element in website to click
    """

    elem = chrome_driver.find_element_by_xpath(xpath=xpath)
    elem.click()


def toggle_all_keys_to_true(chrome_driver: webdriver.Chrome,
                            is_default_layout: bool):
    """
    Toggles all keys to true for the IPO guide website
    :param chrome_driver: Selenium Chrome WebDriver object that navigates the website
    :param is_default_layout: bool if page is the default configuration, otherwise function will assume all fields are
                              deselected.
    """

    default_layout_headers = [dfk.CORPORATION,
                              dfk.DATE,
                              dfk.MARKET,
                              dfk.ADVISOR,
                              dfk.N_FLAGS,
                              dfk.TOTAL_OFFER,
                              dfk.OUTCOME_TO_DATE]

    toggle_table_path = "/html/body/main/section[2]/div[1]"
    soup = bs4.BeautifulSoup(chrome_driver.page_source, "html.parser")
    toggle_table = soup.find(class_="table-column-toggles js-table-column-toggles")
    toggle_columns = toggle_table.find_all(class_="table-column-toggles__column")
    for column_ind, toggle_column in enumerate(toggle_columns):
        toggle_column_path = toggle_table_path + f"/div[{column_ind + 1}]"
        toggle_cells = toggle_column.find_all(class_="table-column-toggles-list__item")
        for cell_ind, toggle_cell in enumerate(toggle_cells):
            label = toggle_cell.get_text()
            label = label.replace("\n", "")
            if is_default_layout:
                if label in default_layout_headers:
                    continue
                else:
                    toggle_cell_path = toggle_column_path + f"/ul/li[{cell_ind + 1}]/input"
                    click_item_at_xpath(chrome_driver=chrome_driver, xpath=toggle_cell_path)
                    print(f"Clicked {label}")
                    time.sleep(1)


def get_ipo_table(driver: webdriver.Chrome,
                  id: str = "datatable_overview") -> bs4.Tag:
    """
    Retrieves a Tag object with the IPO table content.
    :param driver: Selenium Chrome WebDriver object that navigates the website
    :param id: ID for IPO datatable
    :return:
    """

    soup = bs4.BeautifulSoup(driver.page_source, "html.parser")

    table = soup.find(id=id)
    return table


def get_ipo_headers(table: bs4.Tag) -> List[str]:
    """
    Retrieves the header labels from the IPO table.
    :param table: bs4 Tag object for the IPO table
    :return: List with header labels
    """
    header = table.find("thead")
    header_entries = header.find_all("th")
    header_labels = []
    for header_entry in header_entries:
        # The header entry only has one child which is the header label
        for child in header_entry.children:
            header_label = child.strip()     # Remove annoying whitespace and new lines
            header_labels.append(header_label)
    return header_labels


def extract_table_body_to_dict(table: bs4.Tag,
                               header_labels: List[str]) -> Dict[str, str]:
    """
    Extracts content of the IPO table body into a dict where key is header label
    and value is list of entries in the table.
    :param table: bs4.Tag object for the IPO table
    :param header_labels: List with header labels
    :return: Dictionary with table body content separated by header labels.
    """
    df_dict = {header_label: [] for header_label in header_labels}
    body = table.find("tbody")
    table_rows = body.find_all("tr")
    for table_row in table_rows:
        table_cells = table_row.find_all("td")
        for header_label, table_cell in zip(header_labels, table_cells):
            label = table_cell.get_text()
            label = label.replace("\n", " ")
            label = label.replace("\t", "")
            label = label.strip()
            df_dict[header_label].append(label)
    return df_dict


def get_flag_dict(chrome_driver: webdriver.Chrome,
                  table: bs4.Tag,
                  flag_column_ind: int) -> Dict[str, np.ndarray]:
    flag_dict = {}

    body = table.find("tbody")
    table_rows = body.find_all("tr")
    n_ipos = len(table_rows)
    for row_ind, table_row in enumerate(table_rows):
        table_cells = table_row.find_all("td")
        flag_url = table_cells[flag_column_ind].a["href"]
        # Open tab
        chrome_driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
        chrome_driver.execute_script(f'''window.open("{flag_url}","_blank");''')
        # Scroll to get rid of annoying dynamic ad
        chrome_driver.execute_script(f"window.scrollTo(0, {1080})")
        chrome_driver.switch_to.window(chrome_driver.window_handles[1])
        soup = bs4.BeautifulSoup(chrome_driver.page_source, "html.parser")
        flags_pane = soup.find(class_="accordion accordion--small-font")
        flags_list = flags_pane.find_all("li")
        for flags_list_item in flags_list:
            flag_name = flags_list_item.find(class_="accordion-trigger js-accordion-trigger").get_text()
            flag_name = flag_name.strip()
            print(flag_name)
            if flag_name not in flag_dict.keys():
                flag_dict[flag_name] = np.zeros(n_ipos)
            flag_dict[flag_name][row_ind] = 1
        chrome_driver.close()
        chrome_driver.switch_to.window(chrome_driver.window_handles[0])
    return flag_dict
