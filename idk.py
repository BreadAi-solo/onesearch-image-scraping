import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests

# Read the second column of the CSV file
with open('bread.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    column = [row[1] for row in reader]

# Loop through each name in the column
for name in column:
    url = f"https://images.onesearch.com/yhs/search?p={name}+bread"

    # Set up the driver and load the page
    driver = webdriver.Chrome()
    driver.get(url)

    # Scroll down to the bottom of the page and click on "Show more results" button if it exists
    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        try:
            button = driver.find_element("xpath", '//*[@name="more-res"]')
            button.click()
            time.sleep(5)
        except:
            pass
            new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break


    # Get the page source and parse it with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    image_urls = []
    for img in soup.find_all('img'):
        if 'src' in img.attrs:
            image_urls.append(img['src'])

    # Download images
    for i, url in enumerate(image_urls):
        response = requests.get(url)
        try:
            with open(f'{name}_{i}.jpg', 'wb') as f:
                f.write(response.content)
        except OSError as e:
            print(f"Skipping invalid file name: {name}_{i}.jpg")

    driver.quit()
