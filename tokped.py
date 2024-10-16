from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import sys
import io

# Set standard output to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# masukkan link ulasan dari toko yang anda ingin
url = ""

if url:
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    data = []
    for i in range(0, 60):
        soup = BeautifulSoup(driver.page_source, "html.parser")
        containers = soup.findAll('article', attrs={'class': 'css-ccpe8t'})

        for container in containers:
            try:
                review = container.find('span', attrs={'data-testid': 'lblItemUlasan'}).text
                data.append(review)
            except AttributeError:
                continue

        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "button[aria-label^='Laman berikutnya']").click()
        time.sleep(3)

    # Print the DataFrame as a string
    df = pd.DataFrame(data, columns=["Ulasan"])
    print(df.to_string(index=False))  # Print DataFrame as string
    df.to_csv("Tokopedia5.csv", index=False, encoding='utf-8')  # Save D