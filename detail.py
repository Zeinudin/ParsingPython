import json

from pip._internal.models import link
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

url = "https://ev-database.org/"

driver.get(url)


model_list = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "list")))
model_links = model_list.find_elements(By.TAG_NAME, "a")
all_models_data = []

for link in model_links:
    model_data = {}
    if link is not None and link.get_attribute("href"):
        model_url = link.get_attribute("href")

    product_name_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "header.sub-header h1"))
    )
    product_name = product_name_element.text.strip()

    price_table = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "pricing")))

    germany_row = price_table.find_element(By.XPATH, '//a[contains(.,"Germany")]/../following-sibling::td')
    price = germany_row.get_attribute("textContent").strip()

    photo_links = [img.get_attribute("src") for img in driver.find_elements(By.CSS_SELECTOR, ".fotorama__img") if
                   "hqdefault.jpg" not in img.get_attribute("src")]

    data_table = driver.find_element(By.ID, "icons")
    characteristics = [item.text.strip() for item in data_table.find_elements(By.TAG_NAME, "p")]
    processed_characteristics = []
    for characteristic in characteristics:
        if "*" in characteristic:
            characteristic = characteristic.replace("*", "").strip()
        if "span" in characteristic:
            characteristic = characteristic.split("span")[0].strip()
        processed_characteristics.append(characteristic)

    performance_table = driver.find_element(By.ID, "performance")
    performance_rows = performance_table.find_elements(By.TAG_NAME, "tr")
    performance_characteristics = {}
    for row in performance_rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) == 2:
            characteristic = cells[0].text.strip()
            value = cells[1].text.strip()
            performance_characteristics[characteristic] = value

    battery_table = driver.find_element(By.ID, "battery")
    battery_rows = battery_table.find_elements(By.TAG_NAME, "tr")
    battery_characteristics = {}
    for row in battery_rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) == 2:
            characteristic = cells[0].text.strip()
            value = cells[1].text.strip()
            battery_characteristics[characteristic] = value

    charging_table = driver.find_element(By.ID, "charging")
    charging_rows = charging_table.find_elements(By.TAG_NAME, "tr")
    charging_characteristics = {}
    for row in charging_rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) == 2:
            characteristic = cells[0].text.strip()
            value = cells[1].text.strip()
            charging_characteristics[characteristic] = value

    range_table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "range")))
    data_rows = range_table.find_elements(By.TAG_NAME, "tr")
    range_data = {}
    for row in data_rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) == 2:
            category = cells[0].text.strip()
            value = cells[1].text.strip()
            range_data[category] = value

    efficiency_table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "efficiency")))
    data_rows = efficiency_table.find_elements(By.TAG_NAME, "tr")
    efficiency_data = {}
    for row in data_rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) == 2:
            category = cells[0].text.strip()
            value = cells[1].text.strip()
            efficiency_data[category] = value

    model_data = {
        "product_name": product_name,
        "price": price,
        "photo_links": photo_links,
        "characteristics": processed_characteristics,
        "performance": performance_characteristics,
        "battery": battery_characteristics,
        "charging": charging_characteristics,
        "range": range_data,
        "efficiency": efficiency_data
    }

    all_models_data.append(model_data)

driver.quit()

with open("data.json", "w") as json_file:
    json.dump(all_models_data, json_file)

print("Данные всех моделей сохранены в файл data.json.")
