# Phase-02 | 실시간 CryptoPanic 뉴스 수집 자동화 (Airflow Pipeline)


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
- 뉴스 요약문 크롤링

### 🔹 Transform  
- 뉴스 제목/본문 번역 (Google Translate API)  
- UTC → KST 시간 변환  
- 지정 코인 매핑 (**티커 기반, 뉴스:코인 = 1:N 관계**)
- 중복 제거, 50자 미만/내용 누락 뉴스 필터링 (데이터 품질 관리)

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

> 🔸 **10개 코인 선정은 백엔드팀 요청사항**을 기반으로 진행  
> 🔸 총 10개의 코인 티커만 필터링하여 수집  
> 🔸 해당 기준은 향후 비즈니스 요구사항에 따라 유연하게 확장 가능하도록 설계됨

```python
coin_data = [
  (1, "KRW-XRP"), (2, "KRW-BTC"), (3, "KRW-ETH"),
  (4, "KRW-QTUM"), (5, "KRW-WAVES"), (6, "KRW-XEM"),
  (7, "KRW-ETC"), (8, "KRW-NEO"), (9, "KRW-SNT"), (10, "KRW-MTL"),
]
```

---

## 🎥 실시간 뉴스 수집 자동화 시연

> 아래 영상은 Airflow DAG가 5분 주기로 실행
> CryptoPanic API와 Selenium을 통해 실시간으로 뉴스 데이터를 수집
> 지정된 10개 코인 티커에 맞춰 정제된 뉴스가 MySQL에 저장되는 과정

📌 **주요 시연 포인트**:
- Airflow DAG가 **5분 주기로 자동 실행되어 뉴스 크롤링 수행**
- API 수집 → 번역 → 티커 필터링 → DB 저장까지의 전 과정을 **자동화된 파이프라인으로 처리**
- 약 40초 후 MySQL에서 **신규 뉴스 데이터가 저장되어 DB 내용이 갱신된 결과** 확인 가능

[📺 시연 영상 보기] https://drive.google.com/file/d/1fPw5VDxLdeiohLqVFZ8fSORTgpXRK3vx/view?usp=sharing



