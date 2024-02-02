# coding=utf-8
import uvicorn
from fastapi import FastAPI,Header,Body,Form,Request
from fastapi.responses import JSONResponse,HTMLResponse,FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from tortoise.contrib.fastapi import register_tortoise

from dao.models import Todo

app = FastAPI()
template = Jinja2Templates("static")
# 数据库绑定
register_tortoise(app,
                  db_url="mysql://root:admin123@localhost:3306/fastapi",
                  modules={"models":['dao.models']},
                  generate_schemas=True,
                  add_exception_handlers=True,
                  )
# 添加首页
# @app.get("/")
# def index():
#     return "This is Home Page."
@app.get('/users')
def users():
    """获取所有用户"""
    return {"msg":"Get all users","code":2023}
@app.get("/projects")
def project():
    return ["项目1","项目2","项目3"]
# @app.post('/login')
# def login():
#     return {"msg":"login success"}
@app.api_route("/login", methods = ("GET","POST","PUT"))
def login():
    return {"msg":"login success"}
@app.get('/user/{id}')
def user(id):
    return {"id":id}
# @app.get('/user') #用？变量来请求
# def user(id):
#     return {"id":id}
# @app.get('/user')
# def user(id,token = Header(None)):
#     return {"id":id,"token":token}
# @app.post('/login')  #请求可以不一致
# def login(data = Body(None)):
#     return {"data":data}
#表单请求
@app.post('/login')
def login(username=Form(None),passwprd=Form(None) ):#请求徐保持一致
    return {"data":{"username":username,"password":passwprd}}
@app.get('/user')
def user():
    return JSONResponse(content={"msg":"get user"},
                        status_code=202,
                        headers={"a":"b"})
# @app.get("/")
# def index():
#     html_content = """
#     <html>
#         <body><p style="color:red">Hello word</p></body>
#     </html>
#     """
#     return HTMLResponse(content=html_content)
@app.get("/avatar")
def user():
    avatar = 'static/cover.jpg'
    # return FileResponse(avatar,filename="仙剑奇侠传三.jpg")#下载
    return FileResponse(avatar)#不下载
todos = ["写日记","看电影","玩游戏"]#静态
@app.get("/")
async def index(req:Request):#这个需要在地址里请求（动态）
    # 从数据库获取 todos 的代码
    # ORM
    todos = await Todo.all()
    print(todos)
    return template.TemplateResponse("index.html",context={"request":req,"todos":todos})
@app.post("/todo")
async def todo(content=Form(None)):
    """处理用户发过来的 todolist 数据"""
    # todos.insert(0,content)
    # 把新的事项存储到数据库中
    await Todo(content=content).save()
    return RedirectResponse("/",status_code=302)


if __name__ == '__main__':
    uvicorn.run(app)