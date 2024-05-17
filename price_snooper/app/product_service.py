import datetime

import click
import json
import re
from app.utils.request_utils import RequestUtils
from bs4 import BeautifulSoup

from price_snooper.app.dao.price_history_dao import PriceHistoryDao
from price_snooper.app.dao.product_dao import ProductDAO
from price_snooper.app.model.pricehistory import PriceHistory
from price_snooper.app.model.product import Product
from price_snooper.app.utils.constants import GET_PRODUCT_URL, PRODUCT_SEARCH_URL, JSON_HEADER, URL_TO_SCRAPE, \
    DATABASE_NAME
from price_snooper.app.utils.currency import Currency


class ProductService:
    def __init__(self, product_dao):
        self.product_dao = product_dao

    def create_product(self, product_url, expected_discount=0.0):
        payload = json.dumps({
            "url": product_url
        })

        response = RequestUtils.post(PRODUCT_SEARCH_URL, headers=JSON_HEADER, data=payload)
        if response.status_code != 200:
            print("Failed to retrieve webpage")
            return

        data = response.json()
        if data is None or data['status'] == False:
            print("Failed to retrieve product")
            return

        response = RequestUtils.get(GET_PRODUCT_URL.format(url=URL_TO_SCRAPE, product_code=data['code']),
                                    headers=JSON_HEADER)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.create_product_price_objects(soup, product_url, expected_discount)

    def create_product_price_objects(self, soup, product_url, expected_discount):
        product_price_str = soup.find('div', attrs={'title': 'Product selling price'}).text
        currency = self.identify_currency_str(product_price_str[0])
        product_current_price = int(''.join(filter(str.isdigit, product_price_str)))
        product_category = self.find_text_by_th_name(soup, 'product-info', 'Category')[0]
        product_name = self.find_text_by_th_name(soup, 'product-info', 'Product Name')[0]
        product_lowest_price = self.find_lowest_price(soup)
        product = Product(product_url, product_name, product_category)
        product.created_at = datetime.datetime.now()
        product_dao = ProductDAO(DATABASE_NAME)
        product_id = product_dao.insert_product(product)
        price_history = PriceHistory(product_id, product_lowest_price, product_current_price, currency,
                                     expected_discount)
        price_history_dao = PriceHistoryDao(DATABASE_NAME)
        price_history_dao.insert_price_history(price_history)

    def scrape_product(self):
        for product_url in ['https://amzn.in/d/82OFVrw']:
            print(product_url)

    def find_lowest_price(self, soup):
        price_element_str = self.find_tr_with_th(soup, 'Lowest Ever Price')
        if price_element_str is None:
            raise Exception("Failed to find lowest price")

        pattern = r'₹([\d,]+)'
        match = re.search(pattern, price_element_str)
        if match:
            number_str = match.group(1)
            number = int(number_str.replace(',', ''))
            return number
        else:
            raise RuntimeError("No lowest price found")

    def find_tr_with_th(self, soup, th_name):
        tr_elements = soup.find_all('tr')
        for tr in tr_elements:
            th_elements = tr.find_all('th')
            for th in th_elements:
                if th.get_text().__contains__(th_name):
                    return tr.get_text()
        return None

    def find_text_by_th_name(self, soup, div_id, th_name):
        # Find the <div> element with id 'product-info'
        product_info_div = soup.find('div', id=div_id)
        if product_info_div:
            # Find all <tr> elements within the <div>
            tr_elements = product_info_div.find_all('tr')
            for tr in tr_elements:
                # Find all <th> elements within the <tr>
                th_elements = tr.find_all('th')
                for th in th_elements:
                    # Check if the text content of the <th> matches the specified name
                    if th.get_text() == th_name:
                        # If the <th> name matches, find the corresponding <td> elements
                        td_elements = tr.find_all('td')
                        # Extract the text content of <td> elements
                        td_text = [td.get_text() for td in td_elements]
                        return td_text  # Return the text content of <td> elements if found
        return None  # Return None if the <div> or matching <th> is not found

    def identify_currency_str(self, currency_symbol):
        if currency_symbol is None:
            raise RuntimeError("Failed to identify currency symbol")

        for currency in Currency:
            if currency.value == currency_symbol:
                return currency.name

        raise RuntimeError("Failed to identify currency symbol")
