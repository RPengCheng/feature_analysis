
from fastapi import FastAPI,UploadFile,File,HTTPException
from fastapi.responses import FileResponse
import uvicorn
import shutil
import os
app = FastAPI()

# 上传JSON文件
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

if __name__ == '__main__':
    uvicorn.run(app,host="0.0.0.0",port=8000)
    """
    终端可以用
    uvicorn FastAPI_server:app --reload
    """