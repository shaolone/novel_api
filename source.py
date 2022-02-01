

from operator import methodcaller
from typing import Dict, List
from typing_extensions import Self
from copy import *
import json
import requests
import logging

from bs4 import BeautifulSoup


class source():

    source = {}

    def __init__(self, path: str) -> None:
        logging.basicConfig(level=logging.INFO  # 设置日志输出格式
                            # , filename="demo.log"  # log日志输出的文件位置和文件名
                            # , filemode="w"  # 文件的写入格式，w为重新写入文件，默认是追加
                            # 日志输出的格式
                            # -8表示占位符，让输出左对齐，输出长度都为8位
                            # 时间输出的格式
                            , format="[%(asctime)s] - [%(name)-25s] - [%(levelname)-9s] - %(filename)-8s : %(lineno)s line - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
                            )
        self.source = self.load_source(path)
        logging.debug(self.source)

    def load_source(self, path: str) -> Dict:
        with open(path, 'r+', encoding='UTF-8') as source:
            return json.loads(source.read())

    def get_search_response(self, search_key: str) -> Self:
        self.search_url = self.source['search']['url'].replace(
            "{search_key}", search_key)
        self.search_response = BeautifulSoup(
            requests.get(self.search_url), 'html.parser')
        logging.info(self.search_url)
        logging.debug(self.search_response)
        return self

    def get_search_list(self) -> Self:
        self.search_list = copy(self.search_response)
        for scrip in self.source['search']['get_search_list_scrip']:
            self.search_list = methodcaller(
                scrip['name'], *scrip['args'], **scrip['kwargs'])(self.search_list)
        logging.debug(self.search_list)
        return self

    def get_search_item(self) -> Self:
        self.search_item_dict = {}
        for item in self.source['search']['get_search_item_scrip']:
            item_soup = copy(self.search_list)
            for scrip in item['scrip']:
                item_soup = methodcaller(
                    scrip['name'], *scrip['args'], **scrip['kwargs'])(item_soup)
                # print(item_soup)
            self.search_item_dict[f"{item['name']}"] = item_soup
        logging.info(self.search_item_dict)
        return self

    def get_catalogue_response(self, catalogue_url) -> Self:
        self.catalogue_response = BeautifulSoup(
            requests.get(catalogue_url), 'html.parser')
        logging.debug(self.catalogue_response)
        return self

    def get_catalogue_list(self, source_scrip) -> Self:
        self.catalogue_list = copy(self.catalogue_response)
        for scrip in source_scrip:
            self.catalogue_list = methodcaller(
                scrip['name'], *scrip['args'], **scrip['kwargs'])(self.catalogue_list)
        logging.info(self.catalogue_list)
        return self

    def get_catalogue_item(self) -> Self:
        self.catalogue_item = {}
        for item in self.source['catalogue']['get_catalogue_list_scrip']:
            item_soup = copy(self.catalogue_list)
            for scrip in item['scrip']:
                item_soup = methodcaller(
                    scrip['name'], *scrip['args'], **scrip['kwargs'])(item_soup)
                # print(item_soup)
            self.catalogue_item[f"{item['name']}"] = item_soup
        logging.info(self.catalogue_list)
        return self

    def get_paragraph_response(self, paragraph_url) -> Self:
        self.paragraph_response = BeautifulSoup(
            requests.get(paragraph_url), 'html.parser')
        logging.debug(self.paragraph_response)
        return self

    def get_paragraph_list(self) -> Self:
        self.paragraph_list = copy(self.paragraph_response)
        for scrip in self.source['catalogue']['get_catalogue_item_scrip']:
            self.paragraph_list = methodcaller(
                scrip['name'], *scrip['args'], **scrip['kwargs'])(self.paragraph_list)
        logging.info(self.paragraph_list)
        return self

    def get_paragraph(self) -> str:
        self.chapter_list = []
        for item in self.paragraph_list:
            soup = copy(item)
            for scrip in self.source['chapter']['get_paragraph_scrip']:
                soup = methodcaller(
                    scrip['name'], *scrip['args'], **scrip['kwargs'])(soup)
            self.chapter_list.append(soup)
        return self
