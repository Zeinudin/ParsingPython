import json
import re

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()
#page 1
#url = "https://ev-database.org/#sort:path~type~order=.rank~number~desc|range-slider-range:prev~next=0~1200|range-slider-acceleration:prev~next=2~23|range-slider-topspeed:prev~next=110~350|range-slider-battery:prev~next=10~200|range-slider-towweight:prev~next=0~2500|range-slider-fastcharge:prev~next=0~1500|paging:currentPage=0|paging:number=18"
#page 2
#url = "https://ev-database.org/#sort:path~type~order=.rank~number~desc|range-slider-range:prev~next=0~1200|range-slider-acceleration:prev~next=2~23|range-slider-topspeed:prev~next=110~350|range-slider-battery:prev~next=10~200|range-slider-towweight:prev~next=0~2500|range-slider-fastcharge:prev~next=0~1500|paging:currentPage=1|paging:number=18"
#page 3
# url = "https://ev-database.org/#sort:path~type~order=.rank~number~desc|range-slider-range:prev~next=0~1200|range-slider-acceleration:prev~next=2~23|range-slider-topspeed:prev~next=110~350|range-slider-battery:prev~next=10~200|range-slider-towweight:prev~next=0~2500|range-slider-fastcharge:prev~next=0~1500|paging:currentPage=2|paging:number=18"
#page 4
#url = "https://ev-database.org/#sort:path~type~order=.rank~number~desc|range-slider-range:prev~next=0~1200|range-slider-acceleration:prev~next=2~23|range-slider-topspeed:prev~next=110~350|range-slider-battery:prev~next=10~200|range-slider-towweight:prev~next=0~2500|range-slider-fastcharge:prev~next=0~1500|paging:currentPage=3|paging:number=18"
#page 5
# url = "https://ev-database.org/#sort:path~type~order=.rank~number~desc|range-slider-range:prev~next=0~1200|range-slider-acceleration:prev~next=2~23|range-slider-topspeed:prev~next=110~350|range-slider-battery:prev~next=10~200|range-slider-towweight:prev~next=0~2500|range-slider-fastcharge:prev~next=0~1500|paging:currentPage=4|paging:number=18"
#page 6
# url = "https://ev-database.org/#sort:path~type~order=.rank~number~desc|range-slider-range:prev~next=0~1200|range-slider-acceleration:prev~next=2~23|range-slider-topspeed:prev~next=110~350|range-slider-battery:prev~next=10~200|range-slider-towweight:prev~next=0~2500|range-slider-fastcharge:prev~next=0~1500|paging:currentPage=5|paging:number=18"
url = "https://ev-database.org/#sort:path~type~order=.rank~number~desc|range-slider-range:prev~next=0~1200|range-slider-acceleration:prev~next=2~23|range-slider-topspeed:prev~next=110~350|range-slider-battery:prev~next=10~200|range-slider-towweight:prev~next=0~2500|range-slider-fastcharge:prev~next=0~1500|paging:currentPage=17|paging:number=18"
driver.get(url)

model_list = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "list")))
model_links = [link.get_attribute("href") for link in model_list.find_elements(By.TAG_NAME, "a")]

all_models_data = []

for model_url in model_links:
    driver.execute_script("window.open('');")  # Открыть новую вкладку
    driver.switch_to.window(driver.window_handles[1])  # Переключиться на новую вкладку
    driver.get(model_url)  # Переход на страницу модели

    product_name_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "header.sub-header h1"))
    )
    product_name = product_name_element.text.strip()

    pricing_table = driver.find_element(By.ID, "pricing")
    rows = pricing_table.find_elements(By.TAG_NAME, "tr")

    euro_price = None

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) == 2:
            country = cells[0].text.strip()
            price = cells[1].text.strip()
            if country == "Germany":
                price_match = re.search(r'\d{1,3}(?:,\d{3})*(?:\.\d+)?', price)
                if price_match:
                    euro_price = float(price_match.group().replace(',', ''))
                break

    photo_links = [img.get_attribute("src") for img in driver.find_elements(By.CSS_SELECTOR, ".fotorama__img") if "hqdefault.jpg" not in img.get_attribute("src")]

    performance_table = driver.find_element(By.ID, "performance")
    performance_tables = performance_table.find_elements(By.TAG_NAME, "table")
    performance_data = {}

    for table in performance_tables:
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) == 2:
                characteristic = cells[0].text.strip()
                value = cells[1].text.strip()
                performance_data[characteristic] = value

    battery_table = driver.find_element(By.ID, "battery")
    battery_tables = battery_table.find_elements(By.TAG_NAME, "table")
    battery_characteristics = {}

    for table in battery_tables:
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) == 2:
                characteristic = cells[0].text.strip()
                value = cells[1].text.strip()
                battery_characteristics[characteristic] = value

    charging_table = driver.find_element(By.ID, "charging")
    charging_tables = charging_table.find_elements(By.TAG_NAME, "table")
    charging_data = {}

    for table in charging_tables:
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) == 2:
                characteristic = cells[0].text.strip()
                value = cells[1].text.strip()
                charging_data[characteristic] = value

    range_table = driver.find_element(By.ID, "range")
    range_tables = range_table.find_elements(By.TAG_NAME, "table")
    range_data = {}

    for table in range_tables:
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) == 2:
                situation = cells[0].text.strip()
                value = cells[1].text.strip()
                range_data[situation] = value

    efficiency_table = driver.find_element(By.ID, "efficiency")
    efficiency_tables = efficiency_table.find_elements(By.TAG_NAME, "table")
    efficiency_data = {}

    for table in efficiency_tables:
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) == 2:
                parameter = cells[0].text.strip()
                value = cells[1].text.strip()
                efficiency_data[parameter] = value

    model_data = {
        "product_name": product_name,
        "price": euro_price,
        "photo_links": photo_links,
        "battery": battery_characteristics,
        "performance": performance_data,
        "charging": charging_data,
        "range": range_data,
        "efficiency": efficiency_data,
    }

    all_models_data.append(model_data)

    driver.close()  # Закрыть текущую вкладку
    driver.switch_to.window(driver.window_handles[0])  # Вернуться на первоначальную вкладку

driver.quit()

with open("json/data17.1.json", "w") as json_file:
    json.dump(all_models_data, json_file)

print("Данные всех моделей сохранены в файл data.json.")