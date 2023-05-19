import json
import requests
from bs4 import BeautifulSoup
import re

def parse_and_convert_prices(url):
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        products_container = soup.find('div', class_='list')

        products = []
        for item in products_container.find_all('div', class_='list-item'):
            product_name = item.find('a', class_='title').text.strip()
            price_element = item.find('span', class_='price_buy')
            product_image = item.find('div', class_='img').find('a').find('img').get('data-src')
            product_range = item.find('span', class_='erange_real').text.strip()

            if price_element and price_element.text:
                product_price = price_element.text.strip()
                price_without_symbols = re.sub(r'[^\d.]', '', product_price)
                if price_without_symbols:
                    euro_price = float(price_without_symbols)
            exchange_rate = 1.0765
            dollars_price = round(euro_price * exchange_rate, 2)
            dollars_price_str = "${:,.2f}".format(dollars_price)

            products.append({'name': product_name, 'price': dollars_price_str, 'image': product_image, 'range': product_range})

        json_data = json.dumps(products, ensure_ascii=False)

        print(json_data)
        with open('products.json', 'w', encoding='utf-8') as file:
            file.write(json_data)

        print("Данные сохранены в файл 'products.json'")
    else:
        print("Ошибка при загрузке страницы")

# Вызов функции с передачей URL для парсинга
url = "https://ev-database.org/#sort:path~type~order=.rank~number~desc|range-slider-range:prev~next=0~1200|range-slider-acceleration:prev~next=2~23|range-slider-topspeed:prev~next=110~350|range-slider-battery:prev~next=10~200|range-slider-towweight:prev~next=0~2500|range-slider-fastcharge:prev~next=0~1500|paging:currentPage=0|paging:number=9"
parse_and_convert_prices(url)
