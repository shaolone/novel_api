from typing import *
from typing_extensions import *
from fastapi import FastAPI
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
def search(search_key:str,source_name):
    source = load_source(f"./source/{source_name}.json")
    search_url= source['search']['url'].replace(search_key)
    response = requests.get(search_url)
    return

def load_source(path:str) -> dict:
    with open(path,'r+',encoding='UTF-8') as source:
        return json.loads(source.read())
        
