# coding=utf-8
import json

def generate_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file)

# 生成多个JSON文件
for i in range(10):
    data = {'id': i, 'name': f'Object {i}'}
    file_path = f'./client_upload/file{i}.json'
    generate_json_file(file_path, data)
    print(f'生成文件: {file_path}')