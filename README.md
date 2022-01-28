# novel api
>简单 高效 易扩展 

novel api 一个小说接口api服务 

## 技术栈
- requests 发送请求
- BeautifulSoup4 html解析
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
关于 uvicorn main:app --reload 命令...

uvicorn main:app 命令含义如下:

- main：main.py 文件（一个 Python "模块"）。 

- app：在 main.py 文件中通过 app = FastAPI() 创建的对象。

- --reload：让服务器在更新代码后重新启动。仅在开发时使用该选项。

### 交互式 API 文档

    http://127.0.0.1:8000/docs
你会看到自动生成的交互式 API 文档（由 Swagger UI生成）:
![Swagger UI Docs](/img/Swagger%20UI%20Docs.png)

    http://127.0.0.1:8000/redoc
你会看到另一个自动生成的文档（由 ReDoc 生成）：
![ReDoc Docs](/img/ReDoc%20Docs.png)

## 扩展
### 自定义书源
参照内置书源[xquge_net.json](/source/xquge_net.json)

其中:
~~~json
{"search": {"url": "https://www.xquge.net/search?keyword={search_key}"}}
~~~
搜索关键词用`{search_key}`代替

~~~json
{"search": {
    "get_search_list_scrip": [{
            "name": "find",
            "args": [
                "ul"
            ],
            "kwargs": {
                "class": "rank_ullist"
            }
        },
        {
            "name": "find_all",
            "args": [
                "li"
            ],
            "kwargs": {}
        }]}}
~~~
`get_search_list_scrip`内使用`BeautifulSoup`对象的方法,执行完所有`scrip`后,应返回`List`对象
- `name` 方法名
- `args` 位置参数
- `kwargs` 关键字参数

后文中`get_catalogue_list_scrip`,`get_paragraph_list_scrip`同理

具体可用方法列表请参考[BeautifulSoup文档](https://beautifulsoup.readthedocs.io/zh_CN/v4.4.0/)

~~~json
"get_search_item_scrip": [{
                "name": "book_name",
                "scrip": [{
                        "name": "find",
                        "args": [
                            "div"
                        ],
                        "kwargs": {
                            "class": "rank_bkname"
                        }
                    },
                    {
                        "name": "get_text",
                        "args": [],
                        "kwargs": {}
                    }
                ]
            },
            {
                "..."
            }
        ]
~~~
`get_search_list_scrip`返回的`List`中每个`Item`都执行`get_search_item_scrip`,最后应返回`Str`对象
- `get_search_item_scrip.name` 为API返回信息中的`key`,`value`由`name`对应的`scrip`获取
- `get_search_item_scrip.scrip` 与上文写法相同

支持扩展和自定义

## 授权协议声明
1. 已开源的代码，授权协议采用 AGPL进行发行。
2. 您可以免费使用、修改和衍生代码，但不允许修改后和衍生的代码做为闭源软件发布。
3. 修改后和衍生的代码必须也按照AGPL协议进行流通，对修改后和衍生的代码必须向社会公开。
4. 如果您修改了代码，需要在被修改的文件中进行说明，并遵守代码格式规范，帮助他人更好的理解您的用意。
5. 在延伸的代码中（修改和有源代码衍生的代码中）需要带有原来代码中的协议、版权声明和其他原作者规定需要包含的说明（请尊重原作者的著作权，不要删除或修改文件中的@author信息）。