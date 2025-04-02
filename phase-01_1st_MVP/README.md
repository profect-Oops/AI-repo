# 🚀 Phase 01 - 1st MVP: CryptoPanic 뉴스 크롤링 + 자동화 + 번역

## ✅ 목표
- CryptoPanic API 기반 암호화폐 뉴스 **크롤링**
- SPA 구조 대응 (동적 DOM에서 뉴스 요약문 추출)
- 5분마다 **Airflow 스케줄링 자동화**
- DeepL API로 **영문 뉴스 ➝ 한국어 번역**
- MySQL DB에 자동 저장

---

## 📂 주요 파일

| 파일명 | 설명 |
|--------|------|
| `crawler.py` | CryptoPanic API 호출 + Selenium으로 DOM 요약문 크롤링 |
| `crawl_crypto_dag.py` | Airflow DAG 구성 (5분 주기 자동 실행) |

---

## 🔁 자동화 파이프라인

**Airflow DAG 실행 (5분 주기)**  
→ `crawler.py` 실행 (뉴스 크롤링)  
→ `title_en`, `content_en` 확보 (영문 원문)  
→ DeepL API로 번역 → `title`, `content` 생성 (한글)  
→ MySQL DB 저장

---

## 🔬 SPA 구조 대응 전략 (CryptoPanic)

CryptoPanic은 SPA(Single Page Application) 구조로,
일부 정보만 JSON API로 노출됨.  
**뉴스 요약문은 메인 페이지 내 DOM에 숨겨져 있음.**

### ✅ 크롤링 방식
- CryptoPanic API로 뉴스 제목, 링크 확보
- Selenium으로 제목 클릭 이벤트 실행 → 동적 DOM에서 요약문 추출
- 요약문 내 출처 링크는 외부 뉴스사이트로 연결됨  
  ➝ **원문 뉴스 전체는 크롤링 대상에서 제외**

---

## 💭 회고

- 본 Phase에서는 **ML 학습/라벨링 없이**,  
  데이터 수집 → 자동화 → 번역 → 저장까지의 **엔드-투-엔드 파이프라인** 완성
- 다음 Phase에서 모델 학습 및 자동 라벨링으로 확장 예정

---

## 💡 요약 포인트
- ✅ SPA 대응 완료
- ✅ 자동 수집 (Selenium)
- ✅ 5분 스케줄링 (Airflow)
- ✅ 번역 자동화 (DeepL API)
- ✅ DB 저장 자동화 (MySQL)
