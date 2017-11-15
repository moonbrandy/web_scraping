from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import time
import csv


def scrap_trademe_car(car_info_list, output_file_path):

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

        # break

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
            print("Looks like we are on the last page!!")
            driver.close()
            break

    print("we have %s URLs ready for scrap" % len(urls))
    
    headers = ["TITLE", "SUB_TITLE", "LOCATION", "ID", "PRICE", "DEALER_NAME", "DEALER_LOCATION", "ORC", "FUEL_TYPE", "KILOMETRES", "ENGINE_SIZE", "TRANSMISSION", "BODY", "DESCRIPTION"]

    data_output = [headers]

    index_number = 1

    for url in urls:
        row = car_detail_scrap(url)
        data_output.append(row)
        print(row)
        print('we have finished %s URLs' % index_number)
        index_number++

    with open(output_file_path, "w", newline='') as output_file:
        wr = csv.writer(output_file, delimiter=',')
        wr.writerows(data_output)

    print("finished scraping!!")


def clean_string(old_str):
    new_str = old_str.replace('\n', '').replace(',', ';')
    return new_str

def car_detail_scrap(url):

    print('opening webdriver')
    driver = webdriver.PhantomJS()
    driver.wait = WebDriverWait(driver, 3) #wait for website fully loaded
    driver.get(url)

    row = [0] * 14
    try:
        row[0] = clean_string(driver.find_element_by_xpath('//*[@id="ListingTitleBox_TitleText"]').text)
    except NoSuchElementException:
        row[0] = "NA"
        pass

    try:
        row[1] = clean_string(driver.find_element_by_xpath('//*[@id="ListingTitleBox_SubtitleText"]').text)
    except NoSuchElementException:
        row[1] = "NA"
        pass

    try:
        row[2] = clean_string(driver.find_element_by_xpath('//*[@id="ListingTitleBox_LocationText"]').text)
    except NoSuchElementException:
        row[2] = "NA"
        pass

    try:    
        row[3] = clean_string(driver.find_element_by_xpath('//*[@id="ListingDetails"]/div[2]/div/div[2]/div[1]').text).replace('Listing #: ', '')
    except NoSuchElementException:
        row[3] = "NA"
        pass

    try:
        row[4] = clean_string(driver.find_element_by_xpath('//*[@id="AskingPrice_AskingPriceValue"]').text).replace('$', '').replace(';', '')
    except NoSuchElementException:
        row[4] = "NA"
        pass

    try:
        row[5] = clean_string(driver.find_element_by_xpath('//*[@id="DealerProfileBox_dealerName"]').text)
    except NoSuchElementException:
        row[5] = "NA"
        pass

    try:
        row[6] = clean_string(driver.find_element_by_xpath('//*[@id="DealerProfileBox_address"]').text)
    except NoSuchElementException:
        row[6] = "NA"
        pass

    try:
        row[7] = clean_string(driver.find_element_by_xpath('//*[@id="AttributesDisplay_attributesSection"]/ul/li[1]/div[2]/span').text)
    except NoSuchElementException:
        row[7] = "NA"
        pass

    try:
        row[8] = clean_string(driver.find_element_by_xpath('//*[@id="AttributesDisplay_attributesSection"]/ul/li[4]/div[2]/span').text)
    except NoSuchElementException:
        row[8] = "NA"
        pass

    try:   
        row[9] = clean_string(driver.find_element_by_xpath('//*[@id="AttributesDisplay_attributesSection"]/ul/li[2]/div[2]/span').text).replace('km', '').replace(';', '')
    except NoSuchElementException:
        row[9] = "NA"
        pass

    try:
        row[10] = clean_string(driver.find_element_by_xpath('//*[@id="AttributesDisplay_attributesSection"]/ul/li[5]/div[2]/span').text).replace('cc', '').replace(';', '')
    except NoSuchElementException:
        row[10] = "NA"
        pass

    try:
        row[11] = clean_string(driver.find_element_by_xpath('//*[@id="AttributesDisplay_attributesSection"]/ul/li[6]/div[2]/span').text)
    except NoSuchElementException:
        row[11] = "NA"
        pass

    try:
        row[12] = clean_string(driver.find_element_by_xpath('//*[@id="AttributesDisplay_attributesSection"]/ul/li[3]/div[2]/span').text)
    except NoSuchElementException:
        row[12] = "NA"
        pass

    try:
        row[13] = clean_string(driver.find_element_by_xpath('//*[@id="DetailTabs_mainListingDetailTabContentBoxdescription"]').text)
    except NoSuchElementException:
        row[13] = "NA"
        pass

    driver.close()

    return row

GOLF = {'car_type': 4, 'car_make': 75, 'car_model': 12}

OUTPUT_PATH = "output_%s.csv" % time.strftime("%Y_%m_%d_%H")

scrap_trademe_car(GOLF, OUTPUT_PATH)





