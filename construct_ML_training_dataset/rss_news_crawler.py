import feedparser
import requests
import pymysql
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re

# ✅ Google Translate API Key (로컬 테스트용)
GOOGLE_API_KEY = "AIzaSyCnATcu8KTY0leIWWh4AUg-xHb179I1bhA"
TRANSLATE_URL = "https://translation.googleapis.com/language/translate/v2"

# ✅ MySQL 연결 설정
conn = pymysql.connect(
    host='localhost',
    port=3307,
    user='crypto_user',
    password='123456789',
    db='crypto_db',
    charset='utf8mb4'
)
cursor = conn.cursor()

# ✅ RSS Feed 목록
rss_urls = [
    'https://cryptonews.com/news/feed',
    'https://cointelegraph.com/rss',
    'https://bitcoinist.com/feed/',
    'https://cryptoslate.com/feed/',
    'https://news.bitcoin.com/feed/',
    'https://decrypt.co/feed',
    'https://www.coindesk.com/arc/outboundfeeds/rss/',
    'https://bitcoinmagazine.com/feed',
    'https://www.newsbtc.com/feed/',
    'https://cryptopotato.com/feed/',
    'https://u.today/rss',
    'https://zycrypto.com/feed/'
]

# ✅ HTML 제거 함수
def clean_html(raw_html):
    return BeautifulSoup(raw_html, "html.parser").get_text(separator=" ", strip=True)

# ✅ Google Translate 번역 함수
def translate_text(text, target='ko'):
    try:
        if not text.strip():
            return ""
        params = {
            'q': text,
            'target': target,
            'format': 'text',
            'key': GOOGLE_API_KEY
        }
        response = requests.post(TRANSLATE_URL, data=params, timeout=10)
        response.raise_for_status()
        return response.json()['data']['translations'][0]['translatedText']
    except Exception as e:
        print(f"\n❌ 번역 실패: {e}")
        return text

# ✅ 콘텐츠 유효성 검사 함수 (40자 이하 or 링크만 있는 뉴스 제거)
def is_valid_content(text):
    cleaned = re.sub(r'https?://\S+|www\.\S+|youtube|twitter|x\.com|playlist', '', text, flags=re.IGNORECASE)
    cleaned = re.sub(r'[^\w\s]', '', cleaned)  # 특수문자 제거
    cleaned = cleaned.strip()
    return len(cleaned) > 40

# ✅ 시작
start_time = time.time()
success_count = 0
total_count = 0
data_to_insert = []

for url in rss_urls:
    feed = feedparser.parse(url)
    for entry in feed.entries:
        total_count += 1
        try:
            title_en = entry.get("title", "").strip()
            summary_html = entry.get("summary", "") or entry.get("description", "")
            content_en = clean_html(summary_html)

            # 필터링
            if not is_valid_content(content_en):
                continue

            title_ko = translate_text(title_en)
            content_ko = translate_text(content_en)

            source = entry.get("link", "")
            newspaper = entry.get("source", {}).get("title", "News")

            pub_time_str = entry.get("published", "") or entry.get("pubDate", "")
            try:
                pub_time = datetime.strptime(pub_time_str, "%a, %d %b %Y %H:%M:%S %z").astimezone().replace(tzinfo=None)
            except:
                pub_time = datetime.utcnow()

            data_to_insert.append((
                title_ko[:5000],
                content_ko[:10000],
                title_en[:5000],
                content_en[:10000],
                newspaper[:100],
                source[:1000],
                pub_time
            ))
            success_count += 1
        except Exception as e:
            print(f"❌ 파싱 또는 번역 실패: {e}")
            continue

# ✅ DB 저장
insert_query = """
    INSERT INTO rss_news_storage
    (title, content, title_en, content_en, newspaper, source, pubTime)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

try:
    if data_to_insert:
        cursor.executemany(insert_query, data_to_insert)
        conn.commit()
except Exception as e:
    print(f"❌ 벌크 인서트 실패: {e}")

# ✅ 마무리
end_time = time.time()
elapsed = round(end_time - start_time, 2)
print(f"\n✅ 총 {success_count}건 저장 완료 / 전체 {total_count}건 시도")
print(f"⏱ 소요 시간: {elapsed}초")

cursor.close()
conn.close()

