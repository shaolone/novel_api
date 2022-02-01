from operator import methodcaller
from typing import *
from typing_extensions import *
from bs4 import BeautifulSoup
from fastapi import FastAPI
from copy import *
import os
import json
import requests
from source import source

# TODO 补全注释
app = FastAPI()


@app.get('/')
def get_root():
    # TODO 跳转文档页面
    return "Hello Novel Api"


@app.get("/get_source_list")
def get_source_list():
    return os.listdir("./source")


@app.get("/search")
def search(search_key: str, source_name: str):
    """
    通过关键词搜索书源中书籍

    parameters:
        search_key - 搜索的关键词
        source_name - 搜索的书源
    """
    # TODO 多线程遍历书源搜索
    # TODO 异常处理
    return source(f"./source/{source_name}.json").get_search_response(search_key).get_search_list().get_search_item().search_item_dict


@app.get("/catalogue")
def get_catalogue(source_name: str, catalogue_url: str) -> List:
    return source(f"./source/{source_name}.json").get_catalogue_response(
        catalogue_url).get_catalogue_list().get_catalogue_item().catalogue


@app.get("/chapter")
def get_chapter(source_name: str, chapter_url: str) -> List:
    return source(f"./source/{source_name}.json").get_paragraph_response(chapter_url).get_paragraph_list().get_paragraph().paragraphs
