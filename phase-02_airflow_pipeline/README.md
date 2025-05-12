# Phase-02 | 실시간 CryptoPanic 뉴스 수집 자동화 (Airflow 기반)


---

## 🎯 목표

- CryptoPanic API 기반으로 암호화폐 뉴스 실시간 수집
- SPA 구조 대응 (Selenium 활용 DOM 추출)
- 뉴스 요약 및 전체 본문 수집 → 번역 → 코인 매핑
- 5분마다 Airflow DAG로 자동 실행
- MySQL DB에 정제된 뉴스 저장

---

## ⚙️ 주요 구성 파일

| 파일명 | 설명 |
|--------|------|
| `crypto_crawler.py` | CryptoPanic API + Selenium 크롤러 |
| `crawl_crypto_dag.py` | Airflow DAG 파일 (5분마다 자동 실행) |

---

## 🧩 파이프라인 구조 (ETL)

### 🔹 Extract  
- CryptoPanic API 및 Selenium으로 뉴스 수집  
- *뉴스 요약문 크롤링*

### 🔹 Transform  
- 뉴스 제목/본문 번역 (Google Translate API)  
- UTC → KST 시간 변환  
- 지정 코인 매핑 (티커 기반)
- 중복 제거, 50자 미만/내용 누락 뉴스 필터링

### 🔹 Load  
- 정제된 뉴스 → `news` 테이블 저장

---

## 🔁 자동화 구성

- `crawl_crypto_dag.py` DAG 설정
  - schedule_interval: `"*/5 * * * *"` → 5분마다 실행
  - PythonOperator로 `crypto_crawler.py` 실행
- Airflow를 통해 **5분 단위 자동 수집 및 저장**
- 중복 방지 및 다중 코인 연결 처리

---

## 🔍 코인 티커 필터링

> 🔸 **티커 선정은 백엔드팀 요청사항**을 기반으로 진행  
> 🔸 총 10개의 코인 티커만 필터링하여 수집  
> 🔸 해당 기준은 향후 비즈니스 요구사항에 따라 유연하게 확장 가능하도록 설계됨

```python
coin_data = [
  (1, "KRW-XRP"), (2, "KRW-BTC"), (3, "KRW-ETH"),
  (4, "KRW-QTUM"), (5, "KRW-WAVES"), (6, "KRW-XEM"),
  (7, "KRW-ETC"), (8, "KRW-NEO"), (9, "KRW-SNT"), (10, "KRW-MTL"),
]
