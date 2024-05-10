'''
scraper
~~~~~~~

This module contains functions to connect and scrap https://www.pyphoy.com
'''

# Built-in imports
import logging, sys, os, json, re
# External libraries
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.common.by import By

PYPHOY_URL = 'https://www.pyphoy.com'

# Select source of categories

def load_categories_map(relative_path:str):
    '''
    Loads json file into memory to parse and map categories and other assests to display.
    '''
    categories_file = os.path.join(os.path.dirname(__file__), relative_path)
    with open(categories_file, "r", encoding="utf8") as cat_file:
        categories_map = json.load(cat_file)
        cat_file.close()

    return categories_map

def get_cities() -> dict:
    '''
    Scraps the root page of https://www.pyphoy.com and itarates over all of its "option" tags.

    local variables:
        - _cities_matrix -> [["Bogotá", "/bogota"]]

    Returns

    Dictionary version of "_cities_matrix"

    {"Bogotá": "/bogota"}

    TODO:   Excluding Armenia and Cúcuta cities because its fn:get_pyp_info uses dsistrict 
            distinctions not covered by the code funcionality.
    '''
    home_page = request_pyp_page(PYPHOY_URL)
    _cities_matrix = [[t.text, t.attrs['value']] for t in home_page.find_all('option') if t.attrs.get('value')]
    del home_page
    
    return {k: v for k, v in _cities_matrix if not bool(re.search(k,"^(Armenia|Cúcuta)$")) }

def get_categories_in_use(cg_map:dict, city_url:str) -> list:
    '''
    From the bfsoup page requested using "city_url" get the categories that specific city has.
    params:
        - cg_map    -> The loaded category mapa gotten from fn:load_categories_map
        - city_url  -> String url that uses the city to get the info from, E.g. "https://www.pyphoy.com/bogota" 

    returns:
        - A list of the filtered categories in use. E.g.
            ['0', '1', '2']  
    '''
    city_page = request_pyp_page(city_url)
    _cities_text = ['/' + c.find('a').get('href').split("/", 2)[-1] for c in city_page.find_all("h2", {"class": "sc-d159082d-0"})]

    return [c for c in cg_map if cg_map[c]['path'] in _cities_text]
    

def get_pyp_info(url):
    '''
    With a complete version of the url E.g. "url"=https://www.pyphoy.com/bogota/particulares get information
    about the prohibitions for vehicles in the city.

    params:
        - url       -> https://www.pyphoy.com/bogota/particulares complete version of the url

    returns:
        - After searching in Selenium's object DOM for the banned times and plate numbers will produce
        something like:
            {"plate_num": "5-6-7-8-9-0", "banned_times": "7am a 7pm"}
    '''
    options = ChromiumOptions()
    options.add_argument('--headless')
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--remote-debugging-pipe")
    driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=options)
    driver.get(url)
    
    plate_nums_info = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[3]/main/article/div[1]/div[1]/div/div/div[2]').text
    
    if not driver.find_elements(By.CSS_SELECTOR, 'div.gtAiTL'):
        banned_times = [e.text for e in driver.find_elements(By.CSS_SELECTOR, 'div.btujzv')]
    else:
        banned_times = [e.text for e in driver.find_elements(By.CSS_SELECTOR, 'div.gtAiTL')]
    
    driver.close()
    return {'plate_num': plate_nums_info, 'banned_times': banned_times}

def url_builder(*args) -> str:
    '''
    Function that builds an useful url valid for https://www.pyphoy.com

    returns:
        - A string in teh form of "https://www.pyphoy.com/bogota/taxis/fecha/2024-05-02" 
    '''
    base_url, city_path, cat_path, date_path = args
    base_result = base_url + city_path + cat_path
    date_path = '/fecha' + date_path if date_path else ''
    return ( base_result + date_path if date_path else base_result )

def request_pyp_page(pyp_url:str) -> BeautifulSoup:
    '''
    Uses "pyp_url" to initialize a BeautifulSoup using requests.get

    params:
        - pyp_url -> String coming from fn:url_builder.

    returns:
        - A BeautifulSoup object to be parseable.
    '''
    try:
        req = requests.get(pyp_url).content
    except requests.exceptions.ConnectionError as e:
        logging.fatal(f"{e}")
        sys.exit()
    
    pyp_page = BeautifulSoup(req, 'html.parser')
    return pyp_page

def main() -> None:
    pass    
    

if __name__ == "__main__":
    main()