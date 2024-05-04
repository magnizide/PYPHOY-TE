import re
import src.scraper

URL_REGEX = '^((http|https)://)[-a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)$'

ur = re.compile(URL_REGEX)

def test_load_categories_map():
    '''
    TODO
    '''
    test_call = src.scraper.load_categories_map("assets/categories.json")
    assert isinstance(test_call, dict) and len(test_call) > 0

def test_get_cities():
    '''
    TODO
    '''
    test_call = src.scraper.get_cities()

    assert isinstance(test_call, dict) and test_call.get('Bogotá')

def test_url_builder():
    '''
    TODO
    '''
    test_parameters = ('https://www.pyphoy.com',
                    '/bogota',
                    '/taxis',
                    '/2024-01-01'
                    )

    test_call = src.scraper.url_builder(*test_parameters)

    assert isinstance(test_call, str) and re.search(ur, test_call)

def test_request_pyp_page():
    '''
    TODO
    '''
    test_parameter = 'https://www.pyphoy.com/bogota'
    test_call = src.scraper.request_pyp_page(test_parameter)
    tc = test_call.find("div", {"class": "jMHPrL"})

    assert isinstance(test_call, src.scraper.BeautifulSoup) and tc.text == 'PYPHOY'

def test_get_pyp_info():
    '''
    TODO
    '''
    test_parameter = 'https://www.pyphoy.com/bogota/taxis'
    test_call = src.scraper.get_pyp_info(test_parameter)

    assert isinstance(test_call, dict) and test_call.get('plate_num')