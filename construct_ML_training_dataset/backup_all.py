import pandas as pd
import pymysql
from datetime import datetime
import os

# 백업 경로 설정
backup_dir = "/home/user/backup"
os.makedirs(backup_dir, exist_ok=True)

# DB 연결
conn = pymysql.connect(
    host='localhost',
    port=3307,
    user='crypto_user',
    password='123456789',
    db='crypto_db',
    charset='utf8mb4'
)

# 현재 시간
now = datetime.now().strftime("%Y%m%d_%H%M%S")

# ✅ rss_news_storage 백업
try:
    df_rss = pd.read_sql("SELECT * FROM rss_news_storage", conn)
    rss_path = f"{backup_dir}/rss_news_storage_backup_{now}.csv"
    df_rss.to_csv(rss_path, index=False)
    print(f"✅ rss_news_storage 백업 완료 → {rss_path}")
except Exception as e:
    print(f"❌ rss_news_storage 백업 실패: {e}")

# ✅ label_train_data 백업
try:
    df_label = pd.read_sql("SELECT * FROM label_train_data", conn)
    label_path = f"{backup_dir}/label_train_data_backup_{now}.csv"
    df_label.to_csv(label_path, index=False)
    print(f"✅ label_train_data 백업 완료 → {label_path}")
except Exception as e:
    print(f"❌ label_train_data 백업 실패: {e}")

# 연결 종료
conn.close()
