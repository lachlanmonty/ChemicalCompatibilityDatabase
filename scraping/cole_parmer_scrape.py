import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


url = "https://www.coleparmer.com/Chemical-Resistance"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
chem_drop_down_name = "ChemicalListChemical"
mat_drop_down_name = "MaterialListChemical"
chem = soup.find(id=chem_drop_down_name).find_all("option")
mat = soup.find(id=mat_drop_down_name).find_all("option")

# get list of all chemicals and materials in the drop down
chemicals = [i.text for i in chem]
materials = [i.text for i in mat]  # for info
# remove 'Select a Chemical' & 'All Chemicals'
chemicals.remove("Select a Chemical")
chemicals.remove("All Chemicals")


# selenium
browser = webdriver.Firefox()
browser.get(url)
time.sleep(5)

chem_drop_down = Select(browser.find_element("id", chem_drop_down_name))

dfs = []

for chemical in chemicals:

    chem_drop_down.select_by_value(chemical)
    # button class for changing the chemical
    button = r"/html/body/div[5]/div/main/div/div[2]/div/section/section[2]/section[1]/div/div/div[1]/form/div[2]/div[3]/div/button"
    button_select = browser.find_elements("xpath", button)

    button_select[0].click()
    time.sleep(1)
    soup_chem = BeautifulSoup(browser.page_source, "html.parser")

    table = soup_chem.find("table")

    table_body = table.find("tbody")

    data = []
    rows = table_body.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    df = pd.DataFrame(data)
    df = df.rename(columns={0: "material", 1: "compatibility"})
    df["chemical"] = chemical
    dfs.append(df)


cole_data = pd.concat(dfs)
