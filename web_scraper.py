from time import sleep, strftime
from random import randint
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re


class WebScraper:
    def __init__(self, origin, destination):
        self.driver = webdriver.Chrome()
        self.driver.get(f'https://www.kayak.com/flights/{origin}-{destination}/2024-03-11?sort=price_a')

    def __parse_item(self, result_list):
        parsed_result = []
        for i in result_list:
            price = i.find_next('div', class_=re.compile(r'^.{4}-price-text$')).text
            time_list = i.find_next('div', class_=re.compile(r'^.{9}-mod-variant-large$')).find_all('span')
            time = ' '.join([j.text for j in time_list])
            airline = i.find_next('div', class_=re.compile(r'^.{11}-mod-variant-default$')).text
            parsed_result.append({
                'Price': price,
                'Time': time,
                'Airline': airline
            })
        self.driver.close()
        return parsed_result

    def load_data(self):
        sleep(7)
        try:
            path = '//*[@id="listWrapper"]'
            results = WebDriverWait(self.driver, timeout=randint(2, 6)).until(
                EC.presence_of_element_located((By.XPATH, path))).get_attribute(
                'innerHTML')
            soup = BeautifulSoup(results, "html.parser")
            result_list = soup.find_all('div', {'data-resultid': re.compile(r'^[0-9A-Fa-f]{32}$')})
            return self.__parse_item(result_list)
        except:
            try:
                path = 'resultsContainer'
                results = WebDriverWait(self.driver, timeout=randint(2, 6)).until(
                    EC.presence_of_element_located((By.CLASS_NAME, path))).get_attribute(
                    'innerHTML')
                soup = BeautifulSoup(results, "html.parser")
                result_list = soup.find_all('div', {'data-resultid': re.compile(r'^[0-9A-Fa-f]{32}$')})
                return self.__parse_item(result_list)
            except:
                print('Unspecified Error!')