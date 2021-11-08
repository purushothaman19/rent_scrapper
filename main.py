import time
from bs4 import BeautifulSoup
from selenium import webdriver
import requests

GOOGLE_FORM = 'https://docs.google.com/forms/d/e/1FAIpQLScvFcftz8M1rUHS4Q-DDzUM2RUAhsQXsX-L2HEzUl6uDf6v7g/viewform' \
              '?usp=sf_link '
ZILLOW_URL = 'https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C' \
             '%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A' \
             '-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C' \
             '%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A' \
             '%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse' \
             '%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B' \
             '%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D' \
             '%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min' \
             '%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D'

''' BeautifulSoap '''

header = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                  '89.0.4389.82 Safari/537.36',
    "Accept-Language": 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',

}

response = requests.get(ZILLOW_URL, headers=header)
zillow_response = response.text

soup = BeautifulSoup(zillow_response, 'html.parser')
# print(soup)

prices = [price.text.split()[0] for price in soup.find_all(name='div', class_='list-card-price')]
# print(len(prices))

links = [link.get('href') for link in soup.find_all(name='a', class_='list-card-link list-card-link-top-margin')]
print(links)

addresses = [address.text for address in soup.find_all(name='address', class_='list-card-addr')]
# print(type(addresses[0]))

''' Selenium '''

driver = webdriver.Chrome(executable_path='/Users/purush/Development/chromedriver')
driver.get(GOOGLE_FORM)

time.sleep(2)


for i in range(len(links)):
    fill_ups = driver.find_elements_by_css_selector('.quantumWizTextinputPaperinputInput.exportInput')

    time.sleep(1)
    address = fill_ups[0]
    address.click()
    time.sleep(1)
    address.send_keys(addresses[i])

    price = fill_ups[1]
    price.click()
    time.sleep(1)
    price.send_keys(prices[i])

    link = fill_ups[2]
    link.click()
    time.sleep(1)

    if links[i][0] == '/':
        links[i] = f"https://www.zillow.com{links[i]}"

    link.send_keys(links[i])

    submit = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div')
    submit.click()

    new_response = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    new_response.click()

