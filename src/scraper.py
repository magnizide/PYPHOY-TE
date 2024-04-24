import logging, sys, os, json, re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

PYPHOY_URL = 'https://www.pyphoy.com'

# Select source of categories

def load_categories_map():
    '''
    TODO
    '''
    categories_file = (os.path.join(os.path.dirname(__file__), 'assets/categories.json') if os.environ.get("PYPHOY_TH") == 'dev' else 'PROD_STRING')
    with open(categories_file, "r") as cat_file:
        categories_map = json.load(cat_file)
        cat_file.close()

    return categories_map

def get_cities() -> dict:
    '''
    TODO
    '''
    home_page = request_pyp_page(PYPHOY_URL)
    _cities_matrix = [[t.text, t.attrs['value']] for t in home_page.find_all('option') if t.attrs.get('value')]
    del home_page
    return {k: v for k, v in _cities_matrix if not bool(re.search(k,"^(Armenia|Cúcuta)$")) }

def get_categories_in_use(cg_map, city_url):
    '''
    TODO
    '''
    city_page = request_pyp_page(city_url)
    _cities_text = ['/' + c.find('a').get('href').split("/", 2)[-1] for c in city_page.find_all("h2", {"class": "sc-d159082d-0"})]

    return [c for c in cg_map if cg_map[c]['path'] in _cities_text]
    

def get_pyp_info(url):
    '''
    TODO
    '''
    options = Options()
    options.add_argument('--headless=new') 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
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
    TODO
    '''
    base_url, city_path, cat_path, date_path = args
    base_result = base_url + city_path + cat_path
    date_path = '/fecha' + date_path if date_path else ''
    return ( base_result + date_path if date_path else base_result )

def request_pyp_page(pyp_url:str):
    '''
    TODO
    '''
    try:
        req = requests.get(pyp_url).content
    except requests.exceptions.ConnectionError as e:
        logging.fatal(f'{e}')
        sys.exit()
    
    pyp_page = BeautifulSoup(req, 'html.parser')
    return pyp_page

def main() -> None:
    pass    
    

if __name__ == "__main__":
    main()