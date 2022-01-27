from operator import methodcaller
from typing import *
from typing_extensions import *
from bs4 import BeautifulSoup
from fastapi import FastAPI
from copy import *
import os
import json
import requests
app = FastAPI()


@app.get('/')
def get_root():
    return "Hello Novel Api"


@app.get("/get_source_list")
def get_source_list():
    return os.listdir("./source")


@app.get("/search/{search_key}")
def search(search_key: str, source_name):
    source = load_source(f"./source/{source_name}.json")
    search_url = source['search']['url'].replace("{search_key}", search_key)
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    search_list = get_search_list(
        soup, source['search']['get_search_list_scrip'])
    return_list = []
    for soup in search_list:
        return_list.append(get_search_item(soup, source['search']['get_search_item']))
    return return_list


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
            #print(item_soup)
        return_dict[f"{item['name']}"] = item_soup
    return return_dict
