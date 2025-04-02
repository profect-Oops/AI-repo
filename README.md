# AI-repo
### 📁 AI-repo 구조

<details>
<summary><strong>📂 docker-jenkins 구조</strong></summary>

```
docker-jenkins/
├── cloud_functions/
│   ├── rss_crawler/
│   │   ├── main.py                  ← rss 전용 함수
│   │   ├── requirements.txt
│   ├── cryptocompare_crawler/
│   │   ├── main.py                  ← crypto 전용 함수
│   │   ├── requirements.txt
│   └── register_unified_news/
│       ├── main.py                  ← unified_news 등록용
│       ├── sbert_filter.py
│       ├── requirements.txt
├── cloud_run/
│   ├── app.py                  ← FastAPI 서버 (HTTP Trigger: /run)
│   ├── pipeline_runner.py      ← 전체 파이프라인 실행 흐름
│   ├── version_detector.py     ← 전기/전환기/후기 자동 판단
│   ├── requirements.txt
│   ├── scripts/ 
│   │   ├── train_data_generator.py ✅ GPT/crypto CSV 생성
│   │   ├── data_split.py           ✅ train/valid/test 나눔
│   │   ├── train_finbert.py        ✅ FinBERT 학습 및 저장
│   │   ├── evaluate_model.py       ✅ 모델 성능 평가
├── dags/                      ← (옵션) Airflow용 DAG
│   └── airflow_dag.py         ✅ DAG 등록 시 사용
├── scripts/                   ← 전체 파이프라인 실행 코드
│   ├── gpt_predictor.py       ✅ GPT로 뉴스 예측
│   ├── predict_cryptopanic.py ✅ 실시간 뉴스 예측
├── utils/                     ← 공통 모듈
│   ├── gcs_uploader.py        ✅ GCS 업로드 함수
│   └── db_utils.py            ✅ MySQL insert 유틸 (선택)
├── finbert_model/            ← 모델 학습 후 저장될 폴더
│   └── (pytorch_model.bin 등)
├── configs/
│   └── train_config.yaml      ✅ 하이퍼파라미터 설정
├── notebooks/
│   └── analysis.ipynb         ✅ 분석, 실험용 노트북
├── upload_to_gcs_pipeline.sh ✅ 전체 GCS 업로드 (선택)
├── init_gcs_structure.sh     ✅ GCS 디렉토리 생성
├── .env                      ✅ 환경변수 (BUCKET, VERSION 등)
├── requirements.txt
└── README.md
```

</details>

---
