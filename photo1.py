import requests
import json
from bs4 import BeautifulSoup

#url = 'https://www.akevcar.com/zeekr-001-2023-you-edition-100kwh.html'  # Замените на свой URL

#url = "https://www.akevcar.com/zeekr-001-2023-we-edition-140kwh.html"
# url = "https://www.akevcar.com/zeekr-009-2023-me-edition.html"
# url = "https://www.akevcar.com/zeekr-009-2023-we-edition.html"
url = "https://www.licarco.com/zeekr-x"
response = requests.get(url)
html_content = response.content

# Создание объекта BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Извлечение данных
data = {}
data['product_name'] = soup.find('h1', itemprop='name').text
data['photos'] = [img['src'] for img in soup.find_all('img')]
data['prices'] = {
    '1-9 sets': soup.find('div', class_='productprice').find('h4').text,
    '>=10 sets': soup.find('div', class_='productprice').find_all('h4')[1].text
}
data['description'] = soup.find('div', class_='content-body').text.strip()
data['characteristics'] = {}
table_rows = soup.find('table', class_='ke-zeroborder').find_all('tr')
for row in table_rows:
    cells = row.find_all('td')
    if len(cells) >= 2:  # Проверка наличия ячеек <td>
        characteristic = cells[0].text.strip()
        value = cells[1].text.strip()
        data['characteristics'][characteristic] = value

# Сохранение данных в JSON с кодировкой UTF-8
with open('data4.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print("Сохранен")
