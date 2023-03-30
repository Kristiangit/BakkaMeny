from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import title_contains

# specify the path to the chromedriver executable
chromedriver_path = "/chromedriver_mac64/chromedriver"

def scrapeImg(query) -> list:
# create a new Chrome browser instance
    browser = webdriver.Chrome(chromedriver_path)

    # navigate to the Google search page
    browser.get(
        f"https://www.google.com/search?q={query}&tbm=isch&tbs=il:cl&hl=no&sa=X&ved=0CAAQ1vwEahcKEwjYsOub04D-AhUAAAAAHQAAAAAQAw&biw=1440&bih=709")

    # get past google dumb bot-blocker
    browser.find_element(by=By.TAG_NAME, value="button").click()

    # wait for the page to load
    WebDriverWait(browser, timeout=20).until(title_contains(query))

    # get the page source
    imgDiv = browser.find_element(By.CLASS_NAME, "islrc")
    imgList = imgDiv.find_elements(By.TAG_NAME, "img")
    srcList = []
    for i in range (3):
        srcList.append(imgList[i].get_attribute("src"))

    browser.quit()
    return srcList
scrapeImg("pizza")