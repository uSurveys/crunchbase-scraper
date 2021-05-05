import time
from selenium import webdriver  # Selenium is used to navigate webpages
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup  # BS is used to extract data from pages


def main():
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "none"
    driver = webdriver.Chrome(
        desired_capabilities=caps, executable_path="/opt/homebrew/bin/chromedriver", keep_alive=True)

    # Login
    base_url = 'https://www.crunchbase.com'
    driver.get(base_url + "/login")
    time.sleep(3)

    username = "calderwoodra1113@gmail.com"
    password = "x7JKbh7CV6bVrQp"

    driver.find_element_by_name("email").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_class_name("login").click()
    time.sleep(3)

    # Navigate to my saved search
    driver.get(base_url + '/discover/saved/series-a-and-below-mobile-focused/ef6d6cee-777d-4ba2-8965-8aee5a36592d')
    time.sleep(10)

    # Find the elements we're looking for on this page
    organizations = []
    industries = []
    descriptions = []
    cb_ranks = []
    founders = []
    last_funding_date = []
    downloads_in_last_30_days = []

    # For each page of results, look for the sheet-grid element. If it's missing, wait, then look again.
    # For each row in sheet-grid, parse each cell individually
    # Click the next button if it's enabled, otherwise, exit the loop
    print("organizations,industries,cb rank,founders,last funding date,downloads,descriptions")
    while True:
        # Parse out the table
        content = driver.page_source
        soup = BeautifulSoup(content, "html.parser").find("sheet-grid")
        for j, row in enumerate(soup.find_all("grid-row")):
            for i, cell in enumerate(row.find_all("grid-cell")):
                if i == 1:
                    organizations.append(parse_name(cell).replace(',', ' '))
                elif i == 2:
                    industries.append(parse_industries(cell).replace(',', ' '))
                elif i == 3:
                    descriptions.append(parse_span(cell).replace(',', ' '))
                elif i == 4:
                    cb_ranks.append(parse_link(cell).replace(',', '_'))
                elif i == 5:
                    founders.append(parse_founders(cell).replace(',', ' '))
                elif i == 6:
                    last_funding_date.append(parse_link(cell).replace(',', ''))
                elif i == 7:
                    downloads_in_last_30_days.append(parse_span(cell).replace(',', '_'))

            print(",".join([
                organizations[j],
                industries[j],
                cb_ranks[j],
                founders[j],
                last_funding_date[j],
                downloads_in_last_30_days[j],
                descriptions[j],
            ]))

        if driver.find_element_by_class_name("page-button-next").is_enabled():
            href = driver.find_element_by_class_name("page-button-next").get_attribute("href")
            driver.get(href)
            time.sleep(10)
        else:
            break

    driver.close()


def parse_name(cell):
    div = cell.find("div", {"class": "identifier-label"})
    return div.contents[0]


def parse_industries(cell):
    links = cell.find_all("a")
    industries = ""
    for link in links:
        industries = industries + link.contents[0].strip() + "|"
    return industries


def parse_founders(cell):
    links = cell.find_all("a")
    founders = ""
    for link in links:
        founders = founders + link.contents[0] + "|"
        founders = founders + link['href'] + "|"
    return founders


def parse_span(cell):
    span = cell.find("span")
    return span.contents[0]


def parse_link(cell):
    a = cell.find("a")
    return a.contents[0]


main()
