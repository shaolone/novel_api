# novel api
>简单 高效 易扩展 

novel api 一个小说接口api服务 

## 技术栈
- requests 发送请求
- beautifulsoup4 html解析
- fastapi 构建api

## 使用

### clone本项目 

    git clone
    cd NOVEL_API
### 安装依赖

    pip install -r requirements.txt
### 运行
[uvicorn](https://github.com/encode/uvicorn) 是一个闪电般快速的ASGI服务器，基于uvloop和httptools构建。

    uvicorn main:app --reload
region { 关于 uvicorn main:app --reload 命令...

uvicorn main:app 命令含义如下:

- main：main.py 文件（一个 Python "模块"）。 

- app：在 main.py 文件中通过 app = FastAPI() 创建的对象。

- --reload：让服务器在更新代码后重新启动。仅在开发时使用该选项。
} region 关于 uvicorn main:app --reload 命令...
