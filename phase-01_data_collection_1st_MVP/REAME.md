# Phase 01 - 1st MVP: CryptoPanic 뉴스 크롤링 + 자동화 + 번역

## ✅ 목표
- CryptoPanic API 기반 암호화폐 뉴스 **크롤링**
- SPA 구조 대응 (동적 DOM에서 뉴스 요약문 추출)
- 5분마다 Airflow 스케줄링 자동화
- DeepL API로 영문 뉴스 → 한국어 번역
- MySQL DB에 자동 저장

---

## 📁 주요 파일

| 파일명 | 설명 |
|--------|------|
| `crawler.py` | CryptoPanic API 호출 + Selenium으로 DOM 요약문 크롤링 |
| `crawl_crypto_dag.py` | Airflow DAG 구성 (5분 주기 자동 실행)

---

## 🔁 자동화 파이프라인

```text
[Airflow DAG 실행 (5분 주기)]
→ [crawler.py 실행 → 뉴스 크롤링]
→ [title_en, content_en 확보]
→ [DeepL 번역 → title, content 생성]
→ [MySQL DB 저장]
title_en, content_en: 원문 (영문)

title, content: 번역 결과 (한글)

🔬 SPA 구조 대응 전략 (CryptoPanic)
CryptoPanic은 SPA(Single Page Application) 기반 사이트이며,
일부 정보만 JSON API로 제공되고,
뉴스 요약문은 메인 페이지 내 DOM에 숨겨져 있음.

✅ 크롤링 방식
CryptoPanic API로 뉴스 제목, 링크 확보

Selenium으로 제목 클릭 이벤트 실행 → 동적 DOM에서 요약문 추출

요약문 내 출처 링크는 외부 뉴스사이트로 연결됨
→ 원본 뉴스 전체는 크롤링 대상에서 제외

💬 회고
본 Phase에서는 ML 학습, 라벨링 없이 데이터 수집 및 자동화에 집중

SPA 구조 대응, 번역, 저장까지의 파이프라인을 완성함

이후 단계에서 ML 학습 및 자동 라벨링 모델로 확장 예정

