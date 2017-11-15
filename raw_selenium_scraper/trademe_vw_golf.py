from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import time


def scrap_trademe_car(car_info_list):

    car_type = car_info_list['car_type']
    car_make = car_info_list['car_make']
    car_model = car_info_list['car_model']

    start_url = 'https://trademe.co.nz/'

    print('opening webdriver')
    driver = webdriver.PhantomJS()
    driver.wait = WebDriverWait(driver, 3) #wait for website fully loaded

    print('getting URL')
    driver.get(start_url)

    # clicking through the main pages
    print('nevigate to motors')
    driver.find_element_by_xpath('//*[@id="SearchTabs1_MotorsAnchor"]/a').click()

    # selecting Hatchback, Make, Model
    print('selection car information')
    driver.find_element_by_xpath('//*[@id="5"]').click()
    driver.find_element_by_xpath('//*[@id="5"]/option[%s]' % car_type).click()
    driver.find_element_by_xpath('//*[@id="sidebar-Make"]').click()
    driver.find_element_by_xpath('//*[@id="sidebar-Make"]/option[%s]' % car_make).click()
    driver.find_element_by_xpath('//*[@id="15"]').click()
    driver.find_element_by_xpath('//*[@id="15"]/option[%s]' % car_model).click()

    # clicking on Search
    print('Click Search button')
    driver.find_element_by_xpath('//*[@id="sidebarSearch"]/button').click()

    # Scraping
    print('Now we start scraping!!')

    urls = []
    # each page
    while True:
        # getting the super featured urls. 
        while True:
            try:
                driver.find_element_by_xpath('//*[@id="SuperFeaturesNext"]').click()
                super_feature_url = driver.find_element_by_xpath('//*[@id="SuperFeaturesContainer"]/a[3]').get_attribute("href")
                print(super_feature_url)
                if super_feature_url not in urls:
                    urls.append(super_feature_url)
                else:
                    break
            except NoSuchElementException:
                break

        # getting the highlighted urls.
        for i in range(1, 51):
            try:
                highlighted_url = driver.find_element_by_xpath('//*[@data-ga-identifier="%s"]/ul/li[2]/div/a[@class="dotted"]' % i).get_attribute("href")
                print(highlighted_url)
                urls.append(highlighted_url)
            except NoSuchElementException:
                print('There is no %s element for highlight urls, we move on' % i)

        # wait 5 sec before click on the next page
        time.sleep(5)
        try:
            driver.find_element_by_xpath('//*[@rel="next"][1]').click()
        except NoSuchElementException:
            print("Looks like the job is been finished, I'm closing myself")
            driver.close()
            break

    
    headers = []

    data = [headers]

    for url in urls:
        data.append(car_detail_scrap(url))

def car_detail_scrap(url):
    row = [0] * 20
    row[0] = 
    return row

GOLF = {'car_type': 4, 'car_make': 75, 'car_model': 12}

scrap_trademe_car(GOLF)





