import json

# Открываем JSON-файл
with open("data2.json", "r") as json_file:
    data = json.load(json_file)

# Считаем количество полей "name"
name_count = sum("product_name" in item for item in data)

print("Количество полей 'name':", name_count)
