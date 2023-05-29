import requests
from bs4 import BeautifulSoup as bs
from utils.reformatter import filter_table

from consts import URL

def request() -> bs:
    html = requests.get(URL).text
    soup = bs(html, "lxml")
    return soup

def main():
    soup = request()
    table = soup.select_one("body > div.content-top > div.container > div > div > div.col-lg-9.mb-4 > table")
    for i in filter_table(list(table.stripped_strings)):
        print(i)
        
if __name__ == '__main__':
    main()