import requests
from bs4 import BeautifulSoup
from fp.fp import FreeProxy

import re
import numpy as np
import pandas as pd


class WebScraper:
    __headers__ = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/87.0.4280.88 Safari/537.36'}

    @staticmethod
    def get_proxy():
        while 1:
            proxy = FreeProxy(country_id=['US'], rand=True).get()
            if proxy is not None:
                break
        return proxy

    @staticmethod
    def get_soup(main_url, use_proxy=False, remove_imports=True):
        if use_proxy:
            p = WebScraper.get_proxy()
            response = requests.get(main_url, headers=WebScraper.__headers__, proxies={'http': p, 'https': p})
        else:
            response = requests.get(main_url, headers=WebScraper.__headers__)

        soup = BeautifulSoup(response.content, 'lxml')
        if remove_imports:
            for script in soup(["script", "style"]):  # remove all javascript and stylesheet code
                script.extract()
        return soup

    @staticmethod
    def get_json(url):
        return requests.get(url, headers=WebScraper.__headers__).json()

    '''
    SOME PAGES ONLY HAVE 1 TABLE PER PAGE.
    FIND THAT TABLE AND RETURN IT AS A pd.DataFrame
    '''

    @staticmethod
    def get_single_table_pandas(main_url, table_class_name): 
        soup = WebScraper.get_soup(main_url)
        table = soup.find("table", {"class": table_class_name})
        if table is None: 
            raise ValueError(f"Table Element with class name {table} not found") 
            df = pd.read_html(StringIO(str(table)))[0] return soup, df
