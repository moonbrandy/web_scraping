from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
import time
import csv

OUTPUT_FILE_PATH = "D:\\web_scraping\\rental_property_trademe\\urls_%s.csv" % time.strftime("%Y_%m_%d_%H")
URLS_OUTPUT_PATH = "D:\\web_scraping\\rental_property_trademe\\urls_%s.csv" % time.strftime("%Y_%m_%d_%H")

def scrap_trademe_rental_ppt(output_file_path, save_urls_path):

    start_url = "https://www.trademe.co.nz/property"

    print('opening webdriver')
    driver = webdriver.PhantomJS('C:\\Program Files\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
    driver.wait = WebDriverWait(driver, 1) #wait for website fully loaded

    print('getting URL')
    driver.get(start_url)

    # print('nevigate to property')
    # driver.find_element_by_xpath('//*[@id="SearchTabs1_PropertyAnchor"]/a').click()

    driver.save_screenshot("trademe.png")


    print('selection rental')
    driver.find_element_by_xpath('//*[@id="PropertyToRentToggle"]').click()
    # time.sleep(2)

    print('click on submit button')
    driver.find_element_by_xpath('//*[@id="residentialSectionDiv"]/div[3]/div[2]/button').click()
    # time.sleep(2)

    # Scraping
    print('Now we start scraping!!')

    urls = []

    page = 1
    # each page
    while True:
        # getting the super featured urls. 
        while True:
            try:
                driver.find_element_by_xpath('//*[@id="SuperFeaturesNext"]').click()
                super_feature_url = driver.find_element_by_xpath('//*[@id="SuperFeaturesContainer"]/a[3]').get_attribute("href")
                # print(super_feature_url)
                if super_feature_url not in urls:
                    urls.append(super_feature_url)
                else:
                    break
            except NoSuchElementException:
                break

        # break # uncomment this line when doing debug or testing.

        # getting the highlighted urls.
        for i in range(0, 25):
            if i < 10:
                i = "0%s" % i
            try:
                highlighted_url = driver.find_element_by_xpath('//*[@id="ListView_CardRepeater_ctl%s_card_ctl00_listingCard"]/a' % i).get_attribute("href")
                print(highlighted_url)

                if highlighted_url not in urls:
                    urls.append(highlighted_url)
            except NoSuchElementException:
                print('There is no %s element for highlight urls, we move on' % i)

        # wait 2 sec before click on the next page
        # time.sleep(2)
        try:
            print("we are on page %s" % page)
            driver.find_element_by_xpath('//*[@rel="next"][1]').click()
            page = page + 1
        except NoSuchElementException:
            print("Looks like we are on the last page!!")
            driver.close()
            break
    
    with open(save_urls_path, "w", newline='') as urls_output_file:
        wr = csv.writer(urls_output_file, delimiter=',')
        for url in urls:
            wr.writerow([url])

    print("we have %s URLs ready for scrap" % len(urls))
    


    # Closing driver
    driver.close()


scrap_trademe_rental_ppt(OUTPUT_FILE_PATH, URLS_OUTPUT_PATH)
