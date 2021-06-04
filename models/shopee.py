from models.drivers import Driver
from selenium.webdriver.support.ui import WebDriverWait
import urllib
import logging
from models.handlers.products import Products

class Shopee:
    def __init__(self, log_file=None):
        logging.basicConfig(filename=log_file, format='%(asctime)s %(message)s', datefmt='%I:%M:%S', level=logging.INFO)
        self.__root_url = 'https://shopee.com.br/'
        self.__driver = Driver()
    
    def __build_search_filters(self, filters):
        search_filters = '&'

        regions = filters.get('regions')
        rating = filters.get('rating')

        if len(regions) > 0:
            regions_filter = 'locations='
            for region in regions:
                concat = '%2C' if region not in regions[-1] else '&'
                regions_filter += urllib.parse.quote(region).replace('%', '%25') + concat
            search_filters += regions_filter

        if rating: 
            rating_filter = 'ratingFilter=' + str(rating)
            search_filters += rating_filter + '&'

        return search_filters + 'noCorrection=true' if search_filters != '&' else ''

    def __build_search_url(self, keyword, filters):
        prefix = 'search?keyword='
        keyword = keyword.replace(' ', '%20').lower()
        return self.__root_url + prefix + keyword + filters

    def __fetch(self, browser, handler, search):
        browser.get(search)
        WebDriverWait(
            browser,
            timeout=handler.wait_timeout
        ).until(
            lambda driver: driver.find_element_by_class_name(
                handler.wait_condition
            )
        )
        return browser
    
    def __log_filters(self, product, filters):
        logging.info('[Filter] Product: ' + product)

        regions = filters.get('regions')
        if regions:
            logging.info('[Filter] Regions: ' + str(regions))

        rating = filters.get('rating')
        if rating:
            logging.info('[Filter] Rating: ' + str(rating))
        
        logging.info('------------------')


    def get_product(self, product, filters):
        self.__log_filters(product, filters)
        handler = Products('shopee')
        
        filters = self.__build_search_filters(filters)
        search_url = self.__build_search_url(product, filters)
        
        browser = self.__driver.browser
        browser = self.__fetch(browser, handler, search_url)

        pages = int(browser.find_element_by_class_name('shopee-mini-page-controller__total').text)
        products = handler.parse_from_browser(browser)
        
        logging.info(f'Total Pages: {pages}')
        logging.info('------------------')

        for i in range(pages-1):
            logging.info(f'Fetching data from page {str(i+1)}')
            page_url =  search_url + '&page=' + str(i+1)
            browser = self.__fetch(browser, handler, page_url)
            page_products = handler.parse_from_browser(browser)
            products += page_products
            logging.info(f'Page {str(i+1)} done. Number of products: {len(page_products)}')
            logging.info('------------')
        
        logging.info(f'Done. Total products extracted: {len(products)}')
        return handler.format_products(products)
