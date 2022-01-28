from operator import methodcaller
from typing import *
from typing_extensions import *
from bs4 import BeautifulSoup
from fastapi import FastAPI
from copy import *
import os
import json
import requests


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
    source = load_source(f"./source/{source_name}.json")
    search_url = source['search']['url'].replace("{search_key}", search_key)
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    search_list = get_search_list(
        soup, source['search']['get_search_list_scrip'])
    return_list = []
    for soup in search_list:
        return_list.append(get_search_item(
            soup, source['search']['get_search_item_scrip']))
    # TODO 异常处理
    return return_list


@app.get("/catalogue")
def get_catalogue(source_name: str, catalogue_url: str) -> List:
    catalogue_list = []
    source = load_source(f"./source/{source_name}.json")
    soup = BeautifulSoup(requests.get(catalogue_url).text, 'html.parser')
    for item in get_catalogue_list(soup, source['catalogue']['get_catalogue_list_scrip']):
        catalogue_list.append(get_catalogue_item(
            item, source['catalogue']['get_catalogue_item_scrip']))
    return catalogue_list


@app.get("/chapter")
def get_chapter(source_name: str, chapter_url: str) -> List:
    chapter_list = []
    source = load_source(f"./source/{source_name}.json")
    soup = BeautifulSoup(requests.get(chapter_url).text, 'html.parser')
    for item in get_paragraph_list(soup, source['chapter']['get_paragraph_list_scrip']):
        chapter_list.append(get_paragraph(
            item, source['chapter']['get_paragraph_scrip']))
    return chapter_list


def load_source(path: str) -> Dict:
    with open(path, 'r+', encoding='UTF-8') as source:
        return json.loads(source.read())

def get_search_list(soup, source_scrip) -> List:
    for scrip in source_scrip:
        soup = methodcaller(
            scrip['name'], *scrip['args'], **scrip['kwargs'])(soup)
        # print(soup)
    return soup

def get_search_item(soup, source_scrip) -> Dict:
    return_dict = {}
    for item in source_scrip:
        item_soup = copy(soup)
        for scrip in item['scrip']:
            item_soup = methodcaller(
                scrip['name'], *scrip['args'], **scrip['kwargs'])(item_soup)
            # print(item_soup)
        return_dict[f"{item['name']}"] = item_soup
    return return_dict

def get_catalogue_list(soup, source_scrip) -> List:
    for scrip in source_scrip:
        soup = methodcaller(
            scrip['name'], *scrip['args'], **scrip['kwargs'])(soup)
    return soup

def get_catalogue_item(soup, source_scrip) -> Dict:
    catalogue_item = {}
    for item in source_scrip:
        item_soup = copy(soup)
        for scrip in item['scrip']:
            item_soup = methodcaller(
                scrip['name'], *scrip['args'], **scrip['kwargs'])(item_soup)
            # print(item_soup)
        catalogue_item[f"{item['name']}"] = item_soup
    return catalogue_item

def get_paragraph_list(soup, source_scrip) -> List:
    for scrip in source_scrip:
        soup = methodcaller(
            scrip['name'], *scrip['args'], **scrip['kwargs'])(soup)
    return soup

def get_paragraph(soup, source_scrip) -> str:
    for scrip in source_scrip:
        soup = methodcaller(
            scrip['name'], *scrip['args'], **scrip['kwargs'])(soup)
    return soup
