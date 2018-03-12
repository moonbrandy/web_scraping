from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
import time, datetime, csv

OUTPUT_FILE_PATH = "D:\\web_scraping\\rental_property_trademe\\output_%s.csv" % time.strftime("%Y_%m_%d_%H")


def clean_string(old_str):
    new_str = old_str.replace('\n', '').replace(',', ';')
    return new_str

def scrap_trademe_rental_ppt(output_file_path):

    start_url = "https://www.trademe.co.nz/property"

    print('opening webdriver')
    driver = webdriver.PhantomJS('C:\\Program Files\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
    driver.wait = WebDriverWait(driver, 1) #wait for website fully loaded

    print('getting URL')
    driver.get(start_url)

    driver.save_screenshot("trademe.png")


    print('selection rental')
    driver.find_element_by_xpath('//*[@id="PropertyToRentToggle"]').click()

    print('click on submit button')
    driver.find_element_by_xpath('//*[@id="residentialSectionDiv"]/div[3]/div[2]/button').click()

    # Scraping
    print('Now we start scraping!!')

    urls = []
    headers = ["URL","ADDRESS", "REGION", "BEDROOMS", "BATHROOMS", "LIST_DATE", 
    "AVAILABLE_DATE","RENT", "LISTING"]
    data_output = [headers]

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
            if i != "03":
                data_output.append(property_detail_scrap(driver, i))

        # break # uncomment this line when doing debug or testing. 


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

        if page > 500:
            break
    
    with open(output_file_path, "w", newline='') as output_file:
        wr = csv.writer(output_file, delimiter=',')
        for row in data_output:
            wr.writerow(row)

    print("we have scraped %s rows of data." % len(data_output))
    

def clean_string(old_str):
    new_str = old_str.replace('\n', '').replace(',', ';')
    return new_str

def property_detail_scrap(driver, index):

    try:
        url = driver.find_element_by_xpath('//*[@id="ListView_CardRepeater_ctl%s_card_ctl00_listingCard"]/a' % index).get_attribute("href")
    except NoSuchElementException:
        url = "NA"
        print('There is no %s property, we move on' % index)
        pass

    try:

        address = driver.find_element_by_xpath('//*[@id="ListView_CardRepeater_ctl%s_card_ctl00_listingCard"]/a/div/div[2]/div[2]/div[1]' % index).text
    except NoSuchElementException:
        address = "NA"
        pass

    try:
        region = driver.find_element_by_xpath('//*[@id="ListView_CardRepeater_ctl%s_card_ctl00_listingCard"]/a/div/div[2]/div[2]/div[2]/div[1]/div[1]' % index).text
    except NoSuchElementException:
        region = "NA"
        pass
    
    try:
        bedrooms = driver.find_element_by_xpath('//*[@id="ListView_CardRepeater_ctl%s_card_ctl00_listingBedroomCount"]' % index).text
    except NoSuchElementException:
        bedrooms = "NA"
        pass

    try:
        bathrooms = driver.find_element_by_xpath('//*[@id="ListView_CardRepeater_ctl%s_card_ctl00_listingBathroomCount"]' % index).text
    except NoSuchElementException:
        bathrooms = "NA"
        pass

    try:
        list_date = driver.find_element_by_xpath('//*[@id="ListView_CardRepeater_ctl%s_card_ctl00_listingCard"]/a/div/div[2]/div[1]/div/span' % index).text
        if list_date == "Listed Today":
            list_date = datetime.date.today()
        elif list_date == "Listed Yesterday":
            list_date = datetime.date.today() - datetime.timedelta(days=1)
        else:
            list_date = datetime.datetime.strptime(list_date, "Listed %a, %d %b")
            list_date = list_date.replace(year=2018)
            list_date = list_date.date()
    except NoSuchElementException:
        list_date = "NA"
        pass
    except ValueError:
        list_date = "NA"
        pass

    try:
        available_date = driver.find_element_by_xpath('//*[@id="ListView_CardRepeater_ctl%s_card_ctl00_listingCard"]/a/div/div[2]/div[2]/div[2]/div[1]/div[2]' % index).text
        available_date = datetime.datetime.strptime(available_date, "Available %a %d %b")
        available_date = available_date.replace(year=2018)
        available_date = available_date.date()
    except NoSuchElementException:
        available_date = "NA"
        pass
    except ValueError:
        try:
            available_date = datetime.datetime.utcfromtimestamp(int("".join(filter(str.isdigit, available_date)))/1000).date()
        except ValueError:
            available_date = "NA"
            pass

    try:
        rent = driver.find_element_by_xpath('//*[@id="ListView_CardRepeater_ctl%s_card_ctl00_listingCard"]/a/div/div[2]/div[3]/div[2]' % index).text
        rent = int("".join(filter(str.isdigit, rent)))
    except NoSuchElementException:
        rent = "NA"
        pass

    try:
        listing = driver.find_element_by_xpath('//*[@id="ListView_CardRepeater_ctl%s_card_ctl00_listingCard"]/a/div/div[2]/div[2]/div[2]/div[2]/span' % index).text
    except NoSuchElementException:
        listing = "NA"
        pass

    return [url, address, region, bedrooms, bathrooms, list_date, 
    available_date, rent, listing]

scrap_trademe_rental_ppt(OUTPUT_FILE_PATH)
