from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # chạy không giao diện
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=chrome_options)

# https://www.cophieu68.vn/quote/history.php?cP=1&id=%5Ehastc

def fetch_all_pages_selenium(max_pages=61):
    driver = get_driver()
    all_dfs = []

    for page in range(1, max_pages + 1):
        url = f"https://www.cophieu68.vn/quote/history.php?cP={page}&id=%5Ehastc"
        driver.get(url)
        time.sleep(1)  # đợi render

        soup = BeautifulSoup(driver.page_source, "html.parser")
        tables = pd.read_html(str(soup))

        if len(tables) > 1:
            df = tables[1]
            all_dfs.append(df)
            print(f"✅ Lấy trang {page}: {len(df)} dòng")
        else:
            print(f"⚠️ Không tìm thấy bảng ở trang {page}")

    driver.quit()
    return pd.concat(all_dfs, ignore_index=True)

if __name__ == "__main__":
    df_raw = fetch_all_pages_selenium(max_pages=49)
    df_raw.to_csv("hnx_raw_49pages.csv", index=False)
    print("✅ Đã lưu file: hnx_raw_49pages.csv")