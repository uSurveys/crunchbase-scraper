import time
from selenium import webdriver # Selenium is used to navigate webpages
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup # BS is used to extract data from pages
# import pandas as pd # pandas is used to manipulate and store data

def main():
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "none"
    driver = webdriver.Chrome(desired_capabilities=caps, executable_path="/usr/local/bin/chromedriver")

    # Navigate to the 3DS page and get the html source
    base_url = 'https://www.models-resource.com'
    driver.get(base_url + '/3ds/pokemonxy')
    time.sleep(3)
    content = driver.page_source

    # Find the elements we're looking for on this page
    pokemon_urls = []
    pokemon_names = []
    pokemon_model_url = []

    i = -1
    for sheet in BeautifulSoup(content, 'html.parser').find_all('div', {'class':'updatesheeticons'}):
        # Filter out the elements we don't care about
        i = i + 1
        if (i == 0 or i > 6):
            continue

        for pokemon in sheet.find_all('a'):
            pokemon_urls.append(pokemon['href'])
            pokemon_names.append(pokemon.get_text().strip())

    for p in range(len(pokemon_names)):
        pokemon_url = pokemon_urls[p]
        pokemon_model_url = get_download_url(driver, base_url + pokemon_url)
        print(pokemon_names[p] + ',' + base_url + pokemon_model_url)

    driver.close()

def get_download_url(driver, url):
    driver.get(url)
    time.sleep(3)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    pokemon_url = soup.find('table', {'class':'display'}).find('tr', {'class':'rowfooter'}).find('a')['href']
    return pokemon_url

main()