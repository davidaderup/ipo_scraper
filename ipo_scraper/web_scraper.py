"""
This module contains most code related to scraping the content of IPO guiden
"""

from typing import List, Dict

from selenium import webdriver
import bs4


def get_chrome_driver_for_url(url: str) -> webdriver.Chrome:
    """
    Gets a Chrome WebDriver object for a specified URL.
    :param url: URL to a website
    :return: Chrome WebDriver connected to the URL
    """
    driver = webdriver.Chrome()
    driver.get(url=url)
    return driver


def remove_ad(chrome_driver: webdriver.Chrome) -> None:
    """
    Closes the popup ad that appears when you first open the IPO guiden website
    :param chrome_driver: Selenium Chrome WebDriver object that navigates the website
    """
    # this xpath is hardcoded to the button with text "STÄNG X" for the ad that I encountered when making this,
    # It is a google generated ad so it might be subject to change.
    elem = chrome_driver.find_element_by_xpath(xpath="/html/body/div[5]/div/div/div/button")
    elem.click()


def get_ipo_table(driver: webdriver.Chrome,
                  id: str = "datatable_overview") -> bs4.Tag:

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








