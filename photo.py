import requests
from bs4 import BeautifulSoup
import json

# Отправляем GET-запрос на получение HTML-содержимого страницы
url = 'https://www.akevcar.com/geely-ev?gclid=EAIaIQobChMI0aH559mK_wIVB4RoCR0FmQYrEAAYAiAAEgI-x_D_BwE'  # Замените на свой URL
response = requests.get(url)
html_content = response.content

# Создаем объект BeautifulSoup для парсинга HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Создаем список для хранения данных
data = []

# Находим все элементы с классом "pdt-list-box"
product_boxes = soup.find_all(class_='pdt-list-box')

# Проходимся по каждому элементу и извлекаем фото, название и цены
for box in product_boxes:
    # Извлекаем фото
    image_url = box.find('img')['src']

    # Извлекаем название
    product_name = box.find('h4').text.strip()

    # Извлекаем цены
    price_element = box.find(class_='pdt-list-box-price')
    price_range = price_element.find('b').text.strip()

    # Создаем словарь с данными товара
    product_data = {
        'product_name': product_name,
        'image_url': image_url,
        'price_range': price_range
    }

    # Добавляем словарь в список
    data.append(product_data)

# Сохраняем данные в формате JSON
json_data = json.dumps(data, indent=4)

# Записываем JSON-данные в файл
with open('data.json', 'w') as file:
    file.write(json_data)

print("Данные всех моделей сохранены в файл data.json.")
