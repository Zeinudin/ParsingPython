import json

def remove_duplicates(data):
    unique_items = []
    seen = set()
    for item in data:
        item_json = json.dumps(item, sort_keys=True)
        if item_json not in seen:
            unique_items.append(item)
            seen.add(item_json)
    return unique_items

# Загрузка данных из JSON файла
with open("json/dataDuplicate.json", "r") as json_file:
    all_models_data = json.load(json_file)

# Удаление повторяющихся данных
unique_items = remove_duplicates(all_models_data)

# Запись уникальных данных в новый JSON файл
with open("json/dataDuplicate_unique.json", "w") as json_file:
    json.dump(unique_items, json_file)

print("Повторяющиеся данные удалены. Уникальные данные сохранены в файл data_unique.json.")
