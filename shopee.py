# from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import undetected_chromedriver as webdriver
import pandas as pd
import time

# masukkan link ulasan dari toko yang anda ingin
url = ""


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--use_subprocess")
options.add_argument('--disable-notifications')
options.headless = False
driver = webdriver.Chrome(options=options) 


driver.get(url)
reviews_data = []
time.sleep(100)

for i in range(0,50):
    time.sleep(3)  # Tunggu beberapa detik di setiap halaman
    if driver:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        active_reviews = soup.select('.stardust-tabs-panels__panel[style="display: block;"] .shopee-product-rating__main')
        for review_element in active_reviews:
            product_name_element = review_element.select_one('div[style*="box-sizing: border-box; margin: 15px 0px;"]')
            product_name = product_name_element.text.strip() if product_name_element else "None"
            product_variations_element = review_element.select_one('.Z8yTFp')
            product_variations = product_variations_element.text.strip() if product_variations_element else "None"
            rating_element = review_element.find_parent(class_='shopee-product-rating')
            rating = int(rating_element.select('.icon-rating-solid--active').__len__()) if rating_element else "None"
            username_element = rating_element.select_one('.shopee-product-rating__author-name')
            username = username_element.text.strip() if username_element else "None"
            date_element = rating_element.select_one('.shopee-product-rating__time')
            date_full = date_element.text.strip() if date_element else "None"
            date = date_full.split()[0]
            reviews_product_element = date_element.find_next_sibling('div',
                style="position: relative; box-sizing: border-box; margin: 15px 0px; fontsize: 14px; line-height: 20px; color: rgba(0, 0, 0, 0.87); word-break: breakword; white-space: pre-wrap;")
            reviews_product = reviews_product_element.text.strip() if reviews_product_element else "None"
            reviews_data.append({
                "Product Name": product_name,
                "Variations": product_variations,
                "Rating": rating,
                "Username": username,
                "Date": date,
                "Review": reviews_product
            })

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, '.stardust-tabs-panels__panel[style="display: block;"] .shopee-icon-button.shopee-icon-button--right')
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(3)
        except Exception as e:
            print("Next button not clickable:", e)
            break

driver.quit()
df = pd.DataFrame(reviews_data)
df.to_csv("shopee1.csv", index=False, sep=';')