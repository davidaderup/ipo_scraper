"""
This module contains most code related to scraping the content of IPO guiden
"""


from selenium import webdriver
import bs4
url = "https://www.affarsvarlden.se/ipo-guiden/screener"

# Open URL
driver = webdriver.Chrome()
driver.get(url=url)


# Remove ad
elem = driver.find_element_by_xpath(xpath="/html/body/div[5]/div/div/div/button")
elem.click()

# Navigate to table, I use bs4 since it is easier to parse
soup = bs4.BeautifulSoup(driver.page_source, "html.parser")

table = soup.find(id="datatable_overview")
header = table.find("thead")
header_entries = header.find_all("th")
header_labels = []
for header_entry in header_entries:
    # The header entry only has one child which is the header label
    for child in header_entry.children:
        header_label = child.strip()     # Remove annoying whitespace and new lines
        header_labels.append(header_label)

body = table.find("tbody")
table_rows = body.find_all("tr")
for table_row in table_rows:
    table_cells = table_row.find_all("td")
    for table_cell in table_cells:
        link = table_cell.find("a")
        print("new entry")
        if str(link) != "None":
            print(link.get_text())
        else:
            print(link)
    break

s = ""







