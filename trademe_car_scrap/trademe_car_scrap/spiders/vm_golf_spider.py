import scrapy
from scrapy.http.request import Request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import time

class TRADEME_VW_GOLF_Spider(scrapy.Spider):
    name = "trademe_vw_golf_spider"
    allowed_domains = ['trademe.co.nz']
    start_urls = ['https://trademe.co.nz/']

    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.driver.wait = WebDriverWait(self.driver, 3) #wait for website fully loaded

    def parse(self, response):
        self.driver.get(response.url)

        # clicking through the main pages
        self.driver.find_element_by_xpath('//*[@id="SearchTabs1_MotorsAnchor"]/a').click()
        
        # selecting Hatchback, Make, Model
        self.driver.find_element_by_xpath('//*[@id="5"]').click()
        self.driver.find_element_by_xpath('//*[@id="5"]/option[4]').click()
        self.driver.find_element_by_xpath('//*[@id="sidebar-Make"]').click()
        self.driver.find_element_by_xpath('//*[@id="sidebar-Make"]/option[75]').click()
        self.driver.find_element_by_xpath('//*[@id="15"]').click()
        self.driver.find_element_by_xpath('//*[@id="15"]/option[12]').click()

        # clicking on Search
        self.driver.find_element_by_xpath('//*[@id="sidebarSearch"]/button').click()

        for i in range(1, 11):
            time.sleep(1)
            print(self.driver.find_element_by_xpath('//*[@id="SuperFeaturesContainer"]/a[3]').get_attribute("href"))

