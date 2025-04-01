import pymysql
import os
import joblib
import numpy as np
from dotenv import load_dotenv

# 1. 환경 변수 로드 (.env)
load_dotenv("/opt/airflow/.env")

# 2. pipeline 모델 로드
pipeline_path = "/opt/airflow/models/svm_pipeline_20250401_010208.pkl"
pipeline = joblib.load(pipeline_path)

label_map = {-1: "NEGATIVE", 0: "NEUTRAL", 1: "POSITIVE"}

# 3. DB 설정
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT")),
    "cursorclass": pymysql.cursors.DictCursor
}

# 4. 감성 분석 함수 (SVM 버전)
def analyze_sentiment_with_model(text):
    try:
        label_num = pipeline.predict([text])[0]
        if hasattr(pipeline, "predict_proba"):
            proba = pipeline.predict_proba([text])[0]
            score = float(np.dot(proba, [-1, 0, 1]))
        else:
            score = 0.0  # fallback

        label_str = label_map.get(label_num, "NEUTRAL")
        return score, label_str
    except Exception as e:
        print(f"❌ 예측 실패: {e}")
        return 0.0, "NEUTRAL"

# 5. DB 업데이트 함수
def update_news_sentiment_with_model():
    try:
        print("✅ MySQL 연결 중...")
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()

        print("✅ 감성 분석할 뉴스 조회 중...")
        query = """
        SELECT news_id, title_en, content_en 
        FROM news 
        WHERE news_id NOT IN (SELECT news_id FROM news_sentiment);
        """
        cursor.execute(query)
        news_data = cursor.fetchall()

        if not news_data:
            print("✅ 감성 분석할 뉴스가 없음")
            return 

        print(f"✅ 감성 분석할 뉴스 {len(news_data)}개 찾음!")

        insert_query = """
        INSERT INTO news_sentiment (news_id, sentiment_score, sentiment_label)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE sentiment_score = VALUES(sentiment_score), sentiment_label = VALUES(sentiment_label);
        """

        processed_count = 0  

        for news in news_data:
            news_id, title_en, content_en = news["news_id"], news["title_en"] or "", news["content_en"] or ""
            full_text = f"{title_en}. {content_en}".strip()

            sentiment_score, sentiment_label = analyze_sentiment_with_model(full_text)

            print("=======================")
            print(f"📰 뉴스 ID: {news_id}")
            print(f"📰 제목: {title_en}")
            print(f"📄 본문(200자): {content_en[:200]}...")
            print(f"✅ 감성 분석 결과: {sentiment_label} ({sentiment_score})")
            print("=======================")

            try:
                cursor.execute(insert_query, (news_id, sentiment_score, sentiment_label))
                processed_count += 1
            except pymysql.MySQLError as e:
                print(f"❌ MySQL 저장 오류 (news_id {news_id}): {e}")

        conn.commit()
        print(f"✅ {processed_count}개 감성 분석 완료 및 저장됨!")

    except Exception as e:
        print(f"❌ DB 또는 기타 오류: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("🔹 MySQL 연결 종료")

# 6. 실행
print("🔹 SVM 감성 분석 DAG 실행 준비 완료")
update_news_sentiment_with_model()
