from copy import copy
import json
from typing import Dict, List
from pip import main
import requests
from bs4 import BeautifulSoup
from operator import methodcaller
from pprint import pprint as print

def search(search_key: str, source_name):
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
    return soup


def get_catalogue(source_name: str, catalogue_url: str) -> List:
    catalogue_list = []
    source = load_source(f"./source/{source_name}.json")
    soup = BeautifulSoup(requests.get(catalogue_url).text, 'html.parser')
    for item in get_catalogue_list(soup, source['catalogue']['get_catalogue_list_scrip']):
        catalogue_list.append(get_catalogue_item(
            item, source['catalogue']['get_catalogue_item_scrip']))
    return catalogue_list


def get_chapter(source_name: str, chapter_url: str) -> List:
    chapter_list = []
    source = load_source(f"./source/{source_name}.json")
    soup = BeautifulSoup(requests.get(chapter_url).text, 'html.parser')
    for item in get_paragraph_list(soup, source['chapter']['get_paragraph_list_scrip']):
        chapter_list.append(get_paragraph(
            item, source['chapter']['get_paragraph_scrip']))
    return chapter_list


def load_source(path: str) -> dict:
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
            print(item_soup)
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

def get_paragraph_list(soup,source_scrip) -> List:
    for scrip in source_scrip:
        soup = methodcaller(
            scrip['name'], *scrip['args'], **scrip['kwargs'])(soup)
    return soup


def get_paragraph(soup, source_scrip) -> str:
    for scrip in source_scrip:
        soup = methodcaller(
            scrip['name'], *scrip['args'], **scrip['kwargs'])(soup)
    return soup

if __name__ =="__main__":
    print(get_chapter("xquge_net", "https://www.xquge.net/book/3891/119623343.html"))
