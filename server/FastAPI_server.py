
from fastapi import FastAPI,UploadFile,File,HTTPException
from fastapi.responses import FileResponse
from ariadne import QueryType, graphql_sync, make_executable_schema
from ariadne.asgi import GraphQL
import uvicorn
import shutil
import os
app = FastAPI()

# 上传JSON文件56693 → 57188 [PSH, ACK] Seq=1 Ack=1 Win=8441 Len=20
@app.post("/upload")
async def UploadJson(file:UploadFile = File(...)):
    server_filename = file.filename
    save_path = os.path.join("./server_download",server_filename)
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"Json": "Json uploaded successfully", "filename": file.filename}


# 下载图片资源
@app.get("/download/{filename}")
async def DownloadPic(filename:str):
    file_path = os.path.join(r'server_files', filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404,datail="File not found")
    filenames = os.listdir()
    return FileResponse(file_path)
@app.get("/download/")
async def GetFileNames():
    return os.listdir(r"./server_files")

# # 定义GraphQL模式
# type_defs = """
#     type Query {
#         hello(name: String): String!
#     }
# """
#
# query = QueryType()
#
# @query.field("hello")
# def resolve_hello(_, info, name):
#     return f"Hello, {name}!"
#
# schema = make_executable_schema(type_defs, query)
#
# # 创建FastAPI应用程序
# app = FastAPI()
#
# # 将GraphQL应用添加到FastAPI应用中
# app.add_route("/graphql", GraphQL(schema, debug=True))
if __name__ == '__main__':
    uvicorn.run(app,host="127.0.0.1",port=8000,ssl_keyfile="../crt/server.key", ssl_certfile=r"../crt/server.crt")
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    """
    终端可以用
    uvicorn FastAPI_server:app --reload
    """