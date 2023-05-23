import re
import requests
import json
from bs4 import BeautifulSoup

url = "https://www.licarco.com/zeekr-x"
response = requests.get(url)
html_content = response.content.decode('utf-8')


soup = BeautifulSoup(html_content, 'html.parser')

product_name_element = soup.find('h2')
product_name = product_name_element.text.strip()

image_containers = soup.find_all('div', class_='image-container')
image_urls = [a['src'] for image_container in image_containers for a in image_container.find_all('img')]

price_element = soup.find('div', class_='detail-text').find('span')
price = price_element.text.strip()

# Используем регулярное выражение для извлечения списка особенностей
pattern = r'<li>(.*?)<\/li>'
matches = re.findall(pattern, html_content, re.DOTALL)

# Выводим список особенностей
highlighted_features = matches
for feature in highlighted_features:
    print(feature)

# Power and Speed table
power_speed_table = soup.find('div', class_='examination_detail-list-title').find_next('table')
power_speed_data = {}
for row in power_speed_table.find_all('tr'):
    cells = row.find_all('td')
    if len(cells) == 2:
        key = cells[0].find('h4').text.strip()
        value = cells[1].find('span').text.strip()
        power_speed_data[key] = value

# Battery and Charge table
battery_charge_table = soup.find('div', class_='examination_detail-list-title').find_next('table')
battery_charge_data = {}
for row in battery_charge_table.find_all('tr'):
    cells = row.find_all('td')
    if len(cells) == 2:
        key = cells[0].find('h4').text.strip()
        value = cells[1].find('span').text.strip()
        battery_charge_data[key] = value

# Dimensions table
dimensions_table = soup.find('div', class_='examination_detail-list-title').find_next('table')
dimensions_data = {}
for row in dimensions_table.find_all('tr'):
    cells = row.find_all('td')
    if len(cells) == 2:
        key = cells[0].find('h4').text.strip()
        value = cells[1].find('span').text.strip()
        dimensions_data[key] = value

# Extra Features table
extra_features_table = soup.find('div', class_='examination_detail-list-title').find_next('table')
extra_features_data = {}
for row in extra_features_table.find_all('tr'):
    cells = row.find_all('td')
    if len(cells) == 2:
        key = cells[0].find('h4').text.strip()
        value = cells[1].find('span').text.strip()
        extra_features_data[key] = value

# Сохранение данных в JSON с кодировкой UTF-8
data = {
    'product_name': product_name,
    'image_urls': image_urls,
    'price': price,
    'highlighted_features': highlighted_features,
    'power_speed_data': power_speed_data,
    'battery_charge_data': battery_charge_data,
    'dimensions_data': dimensions_data,
    'extra_features_data': extra_features_data
}

with open('data5.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print("Сохранено")
