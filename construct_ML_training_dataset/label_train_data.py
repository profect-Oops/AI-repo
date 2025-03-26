from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pymysql
import time

TICKERS = ['BTC', 'ETH', 'XRP', 'QTUM', 'WAVES', 'XEM', 'ETC', 'NEO', 'SNT', 'MTL']

conn = pymysql.connect(
    host='localhost',
    port=3307,
    user='crypto_user',
    password='123456789',
    db='crypto_db',
    charset='utf8mb4'
)
cursor = conn.cursor()

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://www.cryptocompare.com/news/list/latest/")

# 뉴스 블록 로딩될 때까지 대기 (명확한 대기 적용)
WebDriverWait(driver, 15).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.item-news"))
)

news_blocks = driver.find_elements(By.CSS_SELECTOR, "div.item-news")
data_list = []

for block in news_blocks:
    try:
        title = block.find_element(By.CSS_SELECTOR, "h3").text.strip()
        summary = block.find_element(By.CSS_SELECTOR, "div.news-body").text.strip()
        sentiment = block.find_element(By.CSS_SELECTOR, "span.news-sentiment").text.strip()
        url = block.get_attribute("data-url") or "https://www.cryptocompare.com/news/list/latest/"
        source = block.find_element(By.CSS_SELECTOR, "div.news-data").text.strip().split("\n")[0]

        found_ticker = None
        for ticker in TICKERS:
            if ticker in summary or ticker in title:
                found_ticker = ticker
                break

        if found_ticker:
            data_list.append((
                source,
                title,
                summary,
                sentiment,
                found_ticker,
                url
            ))
    except Exception as e:
        continue

driver.quit()

if data_list:
    insert_sql = """
    INSERT INTO label_train_data (source, title_en, content_en, sentiment_label, coin_ticker, url)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(insert_sql, data_list)
    conn.commit()
    print(f"✅ {len(data_list)}건 저장 완료")
else:
    print("❌ 저장할 뉴스 없음")

cursor.close()
conn.close()

