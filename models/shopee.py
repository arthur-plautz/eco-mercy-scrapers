from models.drivers import Driver
from selenium.webdriver.support.ui import WebDriverWait
import urllib
from models.handlers.products import Products

class Shopee:
    def __init__(self):
        self.__root_url = 'https://shopee.com.br/'
        self.__driver = Driver()
    
    def __build_search_filters(self, regions=[], rating=None):
        filters = '&'

        if len(regions) > 0:
            regions_filter = 'locations='
            for region in regions:
                concat = '%2C' if region not in regions[-1] else '&'
                regions_filter += urllib.parse.quote(region).replace('%', '%25') + concat
            filters += regions_filter

        if rating: 
            rating_filter = 'ratingFilter=' + str(rating)
            filters += rating_filter + '&'

        return filters + 'noCorrection=true' if filters != '&' else ''

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

    def get_product(self, product, regions=[], rating=None):
        handler = Products('shopee')
        
        filters = self.__build_search_filters(regions=regions, rating=rating)
        search_url = self.__build_search_url(product, filters)
        
        browser = self.__driver.browser
        browser = self.__fetch(browser, handler, search_url)

        pages = int(browser.find_element_by_class_name('shopee-mini-page-controller__total').text)
        products = handler.parse_from_browser(browser)
        
        print(f'Number of Pages: {pages}')

        for i in range(pages-1):
            page_url =  search_url + '&page=' + str(i+1)
            browser = self.__fetch(browser, handler, page_url)
            page_products = handler.parse_from_browser(browser)
            products += page_products
        
        return handler.format_products(products)
