import json

# Открываем каждый JSON-файл и загружаем его содержимое
with open('data1.json', 'r') as file1:
    data1 = json.load(file1)

with open('data2.json', 'r') as file2:
    data2 = json.load(file2)

with open('data3.json', 'r') as file3:
    data3 = json.load(file3)

with open('data4.json', 'r') as file4:
    data4 = json.load(file4)

# Объединяем данные в один общий объект или список
combined_data = {
    'data1': data1,
    'data2': data2,
    'data3': data3,
    'data4': data4
}

# Преобразуем объединенные данные в формат JSON
json_data = json.dumps(combined_data)

# Сохраняем объединенные данные в новый JSON-файл
with open('combined_data.json', 'w') as outfile:
    outfile.write(json_data)

print("Combined done")