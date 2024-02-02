# coding=utf-8
import requests
import os
import json

json_path = r'./client_upload'
# 上传JSON文件
def upload_json(jons):
    for json in jons:
        url = "http://localhost:8000/upload"
        file_path = os.path.join(json_path,json)
        files = {"file":open(file_path,"rb")}
        response = requests.post(url,files=files)
        print(response.json())

#下载图片资源
def download_image(path):
        url = "http://localhost:8000/download/"
        filenames= requests.get(url).content.decode()
        filenames = json.loads(filenames)
        for file in filenames:
            file_url = url + file
            response = requests.get(file_url)
            save_path = os.path.join(path,file)
            if response.status_code == 200:
                with open(save_path,"wb") as f:
                    f.write(response.content)
                print(file +"download successfully")
            else:
                print(f'Failed to download image. Status code :{response.status_code}')

#执行上传和下载操作
if __name__ == '__main__':
    sava_path = r'./client_download/'
    Jsons = os.listdir(json_path)
    upload_json(Jsons)
    download_image(sava_path)