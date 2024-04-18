import logging, sys, os, json
import requests, dotenv
from bs4 import BeautifulSoup

PYPHOY_URL = 'https://www.pyphoy.com'

# Dotenv load
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
dotenv.load_dotenv(dotenv_path)

# Select source of categories

def get_cities(home_page:BeautifulSoup) -> dict:
    '''
    TODO
    '''
    _cities_matrix = [[t.text, t.attrs['value']] for t in home_page.find_all('option') if t.attrs.get('value')]
    del home_page
    return {k: v for k, v in _cities_matrix}

def get_categories():
    categories_file = (os.path.join(os.path.dirname(__file__), 'assets/categories.json') if os.environ.get("PYPHOY_TH") == 'dev' else 'PROD_STRING')
    with open(categories_file, "r") as cat_file:
        categories_data = json.load(cat_file)
        cat_file.close()
    
    return categories_data['categories']

def url_builder(*args) -> str:
    '''
    TODO
    '''
    root_url, city_path, cat_path, date_path = args
    base_result = root_url + city_path + cat_path
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
    parameters = (PYPHOY_URL,'/medellin','/taxis', '/2024-04-18')

    bs_homepage = request_pyp_page(PYPHOY_URL)
    req_pyp_url = url_builder(*parameters)
    bs_req_pyp_url = request_pyp_page(req_pyp_url)
    print(bs_req_pyp_url)
    

if __name__ == "__main__":
    main()