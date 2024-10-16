# from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import undetected_chromedriver as webdriver
import pandas as pd
import time

url = "https://shopee.co.id/buyer/1083776907/rating?shop_id=1083527808"


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--use_subprocess")
options.add_argument('--disable-notifications')
options.headless = False
driver = webdriver.Chrome(options=options) 


driver.get(url)

# # Tunggu hingga elemen yang dibutuhkan ada
# WebDriverWait(driver, 2000).until(
#     EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))  # Ganti dengan selector untuk email
# )

# Tunggu untuk login (masukkan email dan password secara manual)
# time.sleep(2000)  # Waktu tunggu untuk memasukkan email dan password

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


# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
# import pandas as pd
# import sys
# import io

# # Set standard output to UTF-8
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# # masukkan link ulasan dari toko yang anda ingin
# url = ""

# if url:
#     options = webdriver.ChromeOptions()
#     options.add_argument("--start-maximized")
#     driver = webdriver.Chrome(options=options)
#     driver.get(url)

#     data = []
#     for i in range(0, 60):
#         soup = BeautifulSoup(driver.page_source, "html.parser")
#         containers = soup.findAll('article', attrs={'class': 'css-ccpe8t'})

#         for container in containers:
#             try:
#                 review = container.find('span', attrs={'data-testid': 'lblItemUlasan'}).text
#                 data.append(review)
#             except AttributeError:
#                 continue

#         time.sleep(2)
#         driver.find_element(By.CSS_SELECTOR, "button[aria-label^='Laman berikutnya']").click()
#         time.sleep(3)

#     # Print the DataFrame as a string
#     df = pd.DataFrame(data, columns=["Ulasan"])
#     print(df.to_string(index=False))  # Print DataFrame as string
#     df.to_csv("Tokopedia5.csv", index=False, encoding='utf-8')  # Save DataFrame to CSV

# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import pandas as pd
# import sys
# import io

# # Set output standar ke UTF-8
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# url = "https://www.tokopedia.com/psonlineofficialstore/review"

# if url:
#     options = webdriver.ChromeOptions()
#     options.add_argument("--start-maximized")
#     options.add_argument("--headless")  # Jalankan dalam mode headless
#     driver = webdriver.Chrome(options=options)
#     driver.get(url)

#     data = []
#     page_count = 0
#     max_pages = 100  # Total halaman yang ingin diambil

#     while page_count < max_pages:
#         try:
#             # Tunggu hingga elemen ulasan dimuat
#             WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, 'article.css-ccpe8t'))
#             )
            
#             soup = BeautifulSoup(driver.page_source, "html.parser")
#             containers = soup.findAll('article', attrs={'class': 'css-ccpe8t'})

#             for container in containers:
#                 try:
#                     review = container.find('span', attrs={'data-testid': 'lblItemUlasan'}).text
#                     data.append(review)
#                 except AttributeError:
#                     continue

#             # Mencetak jumlah ulasan yang diambil dari halaman ini
#             print(f"Halaman {page_count + 1}: {len(containers)} ulasan diambil.")
#             page_count += 1

#             # Mencoba untuk mengklik tombol berikutnya
#             next_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label^='Laman berikutnya']")
#             next_button.click()
            
#             # Tunggu hingga halaman baru dimuat
#             WebDriverWait(driver, 10).until(
#                 EC.staleness_of(next_button)  # Tunggu hingga tombol menjadi tidak valid setelah diklik
#             )
#         except Exception as e:
#             print("Terjadi kesalahan:", e)
#             break  # Keluar dari loop jika terjadi kesalahan

#     driver.quit()
#     df = pd.DataFrame(data, columns=["Ulasan"])
#     print(df.to_string(index=False))  # Cetak DataFrame sebagai string
#     df.to_csv("Tokopedia1.csv", index=False, encoding='utf-8')  # Simpan DataFrame ke CSV
