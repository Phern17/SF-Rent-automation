from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time

google_form_url = 'https://docs.google.com/forms/d/e/1FAIpQLScFtSB-gL8b2hT97zeHg-IUpgM9r-n-XmeFz01UyuthM-Kdow/viewform?usp=sf_link'

google_chrome_driver = 'C:/Users/User/Downloads/chromedriver_win32/chromedriver.exe'

zillow_url = "https://www.zillow.com/homes/San-Francisco,-CA_rb/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.55177535009766%2C%22east%22%3A-122.31488264990234%2C%22south%22%3A37.69926912019228%2C%22north%22%3A37.851235694487485%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

special_char = ['$', '+', ',', 'm', 'o', '/']

driver = webdriver.Chrome(executable_path=google_chrome_driver)
driver.get(url=google_form_url)

webpage_data = requests.get(url=zillow_url, headers=headers)
soup = BeautifulSoup(webpage_data.text, 'html.parser')
soup = soup.find("div", "result-list-container")

card_info_listing = soup.find_all('div', 'list-card-info')

for item in card_info_listing:
    property_address = item.find('a')
    link = property_address.get('href')
    check_link = link.split('/')[0]
    if check_link == 'https:':
        # address_list.append(address)
        # property_address.address.text
        rental = item.find('div', 'list-card-price').text
        for char in special_char:
            rental = rental.replace(char, '')
        address_input = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        address_input.send_keys(property_address.address.text)
        rental_input = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        rental_input.send_keys(rental)
        link_input = driver.find_element_by_xpath(
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        link_input.send_keys(link)
        submit_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span')
        submit_button.click()
        time.sleep(2)
        submit_another = driver.find_element_by_link_text('Submit another response')
        submit_another.click()
        time.sleep(1)
    else:
        continue

driver.quit()

