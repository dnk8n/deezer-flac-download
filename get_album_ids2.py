from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import time

from selenium.webdriver.edge.service import Service




def get_album_ids(url):
    # Set up the Selenium driver (make sure to specify the correct path to your driver)
    service = Service(r"msedgedriver.exe")
    options = webdriver.EdgeOptions()
    driver = webdriver.Edge(service=service, options=options)
    driver.get(url)

    # Wait for the accept button to be clickable, and then click it
    wait = WebDriverWait(driver, 10)
    accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div/div[2]/div[1]/button')))
    accept_button.click()

    # Give the page 30 seconds to load before scraping
    time.sleep(30)

    # Now that the page is fully scrolled, grab the HTML and use BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    # Find all hrefs that contain 'album/(\d+)'
    album_links = soup.find_all('a', href=re.compile(r'album/(\d+)'))
    
    # Extract the album IDs from the hrefs
    album_ids = [re.search(r'album/(\d+)', a['href']).group(1) for a in album_links]

    return album_ids

# Example usage:
url = 'https://www.deezer.com/en/playlist/12814501181'  # Replace with your URL
print(get_album_ids(url))
