import json

def check_duplicates(data):
    seen = set()
    duplicates = []
    for item in data:
        item_json = json.dumps(item, sort_keys=True)
        if item_json in seen:
            duplicates.append(item)
        else:
            seen.add(item_json)
    return duplicates

# Загрузка данных из JSON файла
with open("json/dataDuplicate.json", "r") as json_file:
    all_models_data = json.load(json_file)

# Проверка наличия повторяющихся данных
duplicate_items = check_duplicates(all_models_data)

if duplicate_items:
    print("Обнаружены повторяющиеся данные:")
    for item in duplicate_items:
        print(item)
else:
    print("Повторяющиеся данные отсутствуют.")
