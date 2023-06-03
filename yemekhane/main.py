import requests
from bs4 import BeautifulSoup as bs
from consts import URL

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from utils.reformatter import filter_table

app = FastAPI(
    description="Yemekhane API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def request() -> bs:
    html = requests.get(URL).text
    return bs(html, "lxml")

def get_json():
    soup = request()
    table = soup.select_one("body > div.content-top > div.container > div > div > div.col-lg-9.mb-4 > table")
    menu = filter_table(list(table.stripped_strings))
    return menu

@app.get("/")
def _index():
    return RedirectResponse("/menu")

@app.get("/menu", response_class=JSONResponse)
def _menu():
    return get_json()
