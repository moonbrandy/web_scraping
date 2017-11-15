import scrapy
from scrapy.http.request import Request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import time


class TechcrunchSpider(scrapy.Spider):
    name = "techcrunch_spider_performance"
    allowed_domains = ['techcrunch.com']
    start_urls = ['https://techcrunch.com/search/heartbleed']



    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1120, 550)
        #self.driver = webdriver.Chrome("C:\Users\Daniel\Desktop\Sonstiges\chromedriver.exe")
        self.driver.wait = WebDriverWait(self.driver, 5)    #wartet bis zu 5 sekunden

    def parse(self, response):
        start = time.time()     #ZEITMESSUNG
        self.driver.get(response.url)

        #wartet bis zu 5 sekunden(oben definiert) auf den eintritt der condition, danach schmeist er den TimeoutException error
        try:    

            self.driver.wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "block-content")))
            print("Found : block-content")

        except TimeoutException:
            self.driver.close()
            print(" block-content NOT FOUND IN TECHCRUNCH !!!")


        #Crawle durch Javascript erstellte Inhalte mit Selenium

        ahref = self.driver.find_elements(By.XPATH,'//h2[@class="post-title st-result-title"]/a')

        hreflist = []
        #Alle Links zu den jeweiligen Artikeln sammeln
        for elem in ahref :
            hreflist.append(elem.get_attribute("href"))


        for elem in hreflist :
            print(elem)



        print("im closing myself")
        self.driver.close()
        end = time.time()
        print("Time elapsed : ")
        finaltime = end-start
        print(finaltime)