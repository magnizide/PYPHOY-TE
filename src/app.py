import logging, sys, os, json
from re import compile
import requests, dotenv
from bs4 import BeautifulSoup

PYPHOY_URL = 'https://www.pyphoy.com'

# Dotenv load
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
dotenv.load_dotenv(dotenv_path)

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

def get_cities(home_page:BeautifulSoup) -> dict:
    '''
    TODO
    '''
    _cities_matrix = [[t.text, t.attrs['value']] for t in home_page.find_all('option') if t.attrs.get('value')]
    del home_page
    return {k: v for k, v in _cities_matrix}

def get_categories_in_use(cg_map, city_page:BeautifulSoup):
    '''
    TODO
    '''
    _cities_text = ['/' + c.find('a').get('href').split("/", 2)[-1] for c in city_page.find_all("h2", {"class": "sc-d159082d-0"})]

    return [c for c in cg_map if cg_map[c]['path'] in _cities_text]
    

def get_pyp_info(pyp_page:BeautifulSoup):
    card = pyp_page.find("div", {"class": "sc-77fa22c1-0 cPRBMS sc-bd02118d-0 izfnOD sc-9e56e907-9 joSnLR"})
    nums_pyp = card.find("div", {"class": "sc-4e15c505-0 juuwzm sc-9e56e907-2 jGMtpa"}).text
    info_pyp = card.find_all("ul", {"class": "sc-f11b3054-3 kvXdBF"})
    print(info_pyp)
    return 

def url_builder(*args) -> str:
    '''
    TODO
    '''
    base_url, city_path, cat_path, date_path = args
    base_result = base_url + city_path + cat_path
    date_path = '/fecha' + date_path if date_path else ''
    return ( base_result + date_path if date_path else base_result )

def request_pyp_page(pyp_url:str):
    try:
        req = requests.get(pyp_url).content
    except requests.exceptions.ConnectionError as e:
        logging.fatal(f'{e}')
        sys.exit()
    
    pyp_page = BeautifulSoup(req, 'html.parser')
    return pyp_page



def main() -> None:
    parameters = (PYPHOY_URL,'/cali','/particulares', '/2024-04-19')

    # bs_homepage = request_pyp_page(PYPHOY_URL)
    req_pyp_url = url_builder(*parameters)
    bs_pyp_req_pyp_url = request_pyp_page(req_pyp_url)
    #categories_map = load_categories_map()
    get_pyp_info(bs_pyp_req_pyp_url)

if __name__ == "__main__":
    main()