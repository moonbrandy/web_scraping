from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
import time
import csv


def scrap_trademe_car(car_info_list, output_file_path, save_urls_path):

    car_type = car_info_list['car_type']
    car_make = car_info_list['car_make']
    car_model = car_info_list['car_model']

    start_url = 'https://trademe.co.nz/'

    print('opening webdriver')
    driver = webdriver.PhantomJS()
    driver.wait = WebDriverWait(driver, 1) #wait for website fully loaded

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
        for i in range(1, 51):
            try:
                highlighted_url = driver.find_element_by_xpath('//*[@data-ga-identifier="%s"]/ul/li[2]/div/a[@class="dotted"]' % i).get_attribute("href")
                # print(highlighted_url)
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
            wr.writerow([urls])

    print("we have %s URLs ready for scrap" % len(urls))
    
    headers = ["TITLE", "SUB_TITLE", "LOCATION", "ID", "PRICE", "DEALER_NAME", "DEALER_LOCATION", "DESCRIPTION",
     "ORC", "NUMBER_PLATE", "KM", "BODY", "FUEL_TYPE", "ENGINE_SIZE", "TRANSMISSION", "HISTORY", "REGISTRATION_EXPIRE", "WOF_EXPIRE", "MODEL_DETAIL",
     "PAGE_VIEW"]

    data_output = [headers]

    index_number = 1

    print('opening webdriver')
    driver = webdriver.PhantomJS()

    for url in urls:
        row = car_detail_scrap(driver, url)
        data_output.append(row)
        # print(row)
        print('we have finished %s URLs' % index_number)
        index_number=index_number + 1

    driver.close()

    with open(output_file_path, "w", newline='') as output_file:
        wr = csv.writer(output_file, delimiter=',')
        wr.writerows(data_output)

    print("finished scraping!!")


def scrap_trademe_car_from_exsist_urls(car_info_list, input_urls_file_path, output_file_path, save_urls_path):

    car_type = car_info_list['car_type']
    car_make = car_info_list['car_make']
    car_model = car_info_list['car_model']

    start_url = 'https://trademe.co.nz/'

    print('opening webdriver')
    driver = webdriver.PhantomJS()
    driver.wait = WebDriverWait(driver, 1) #wait for website fully loaded

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

    with open(input_urls_file_path, newline='') as csvfile:
         csv_reader = csv.reader(csvfile,delimiter=',')
         for row in csv_reader:
             urls.append(row)

    print("we have %s URLs ready for scrap" % len(urls))
    
    headers = ["TITLE", "SUB_TITLE", "LOCATION", "ID", "PRICE", "DEALER_NAME", "DEALER_LOCATION", "DESCRIPTION",
     "ORC", "NUMBER_PLATE", "KM", "BODY", "FUEL_TYPE", "ENGINE_SIZE", "TRANSMISSION", "HISTORY", "REGISTRATION_EXPIRE", "WOF_EXPIRE", "MODEL_DETAIL",
     "PAGE_VIEW"]

    data_output = [headers]

    index_number = 1

    for url in urls:
        row = car_detail_scrap(driver, url)
        data_output.append(row)
        # print(row)
        print('we have finished %s URLs' % index_number)
        index_number+=index_number

    driver.close()

    with open(output_file_path, "w", newline='') as output_file:
        wr = csv.writer(output_file, delimiter=',')
        wr.writerows(data_output)

    print("finished scraping!!")


def clean_string(old_str):
    new_str = old_str.replace('\n', '').replace(',', ';')
    return new_str

def car_detail_scrap(driver, url):

    driver.wait = WebDriverWait(driver, 1) #wait for website fully loaded
    driver.get(url)

    row = [0] * 20
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
        try:
            buy_now = clean_string(driver.find_element_by_xpath('//*[@id="BuyNow_BuyNow"]').text).replace('$', '').replace(';', '')
            current_bidding = clean_string(driver.find_element_by_xpath('//*[@id="Bidding_CurrentBidValue"]').text).replace('$', '').replace(';', '')
            row[4] = str(buy_now) + "-" + str(current_bidding)
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
        row[7] = clean_string(driver.find_element_by_xpath('//*[@id="DetailTabs_mainListingDetailTabContentBoxdescription"]').text)
    except NoSuchElementException:
        row[7] = "NA"
        pass

    try:
        row[8] = clean_string(get_attribute(driver, "On road costs"))
    except NoSuchElementException:
        row[8] = "NA"
        pass

    try:
        row[9] = clean_string(get_attribute(driver, "Number plate"))
    except NoSuchElementException:
        row[9] = "NA"
        pass

    try:
        row[10] = clean_string(get_attribute(driver, "Kilometres")).replace('km', '').replace(';', '')
    except NoSuchElementException:
        row[10] = "NA"
        pass

    try:
        row[11] = clean_string(get_attribute(driver, "Body"))
    except NoSuchElementException:
        row[11] = "NA"
        pass

    try:
        row[12] = clean_string(get_attribute(driver, "Fuel type"))
    except NoSuchElementException:
        row[12] = "NA"
        pass

    try:
        row[13] = clean_string(get_attribute(driver, "Engine size")).replace('cc', '').replace(';', '')
    except NoSuchElementException:
        row[13] = "NA"
        pass

    try:
        row[14] = clean_string(get_attribute(driver, "Transmission"))
    except NoSuchElementException:
        row[14] = "NA"
        pass

    try:
        row[15] = clean_string(get_attribute(driver, "History"))
    except NoSuchElementException:
        row[15] = "NA"
        pass

    try:
        row[16] = clean_string(get_attribute(driver, "Registration expires"))
    except NoSuchElementException:
        row[16] = "NA"
        pass

    try:
        row[17] = clean_string(get_attribute(driver, "WoF expires"))
    except NoSuchElementException:
        row[17] = "NA"
        pass

    try:
        row[18] = clean_string(get_attribute(driver, "Model detail"))
    except NoSuchElementException:
        row[18] = "NA"
        pass

    try:
        view_count_numbers = driver.find_elements_by_xpath('//*[@id="ListingFooter_ViewCount"]/div[2]/span')
        view_count = []
        for number_element in view_count_numbers:
            view_count.append(number_element.text)

        try:
            row[19] = int(''.join(view_count))
        except:
            row[19] = "NA"
            pass
    except NoSuchElementException:
        row[19] = "NA"
        pass

    return row

def get_attribute(driver, KEY):
    all_attributes = driver.find_elements_by_xpath('//*[@id="AttributesDisplay_attributesSection"]/ul/li')

    found_it = False

    for attribute in all_attributes:
        attribute_label = attribute.find_element_by_xpath('.//div[1]/label').text
        if attribute_label == KEY:
            found_it = True
            return attribute.find_element_by_xpath('.//div[2]/span').text
        else:
            continue

    if not found_it:
        return "NA"



GOLF = {'car_type': 4, 'car_make': 75, 'car_model': 12}

OUTPUT_PATH = "output_%s.csv" % time.strftime("%Y_%m_%d_%H")
URLS_OUTPUT_PATH = "urls_%s.csv" % time.strftime("%Y_%m_%d_%H")
# TEST_PATH = "test_%s.csv" % time.strftime("%Y_%m_%d_%H")
FAST_PATH = "fast_%s.csv" % time.strftime("%Y_%m_%d_%H")

scrap_trademe_car(GOLF, FAST_PATH, URLS_OUTPUT_PATH)

# INPUTURL_FILE_PATH = "urls_2017_11_16_15.csv"
# scrap_trademe_car_from_exsist_urls(GOLF, INPUTURL_FILE_PATH, FAST_PATH, URLS_OUTPUT_PATH)



