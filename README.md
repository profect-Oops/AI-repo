# AI-repo
### 📁 AI-repo 구조
![image](https://github.com/user-attachments/assets/6b078172-7658-4a43-9d49-e64d873fa281)

<details>
<summary><strong>📂 docker-jenkins 구조</strong></summary>

```
docker-jenkins/
├── airflow/ 
│   ├── dags/ 
│   │   ├── coin_sentiment_stats.py           #3-1 코인별 감성 점수 통계 계산
│   │   ├── coin_stats_dag.py                 #3-2 코인별 감성 점수 통계 계산 dag
│   │   ├── coin_update.py                    #4-1 최신 코인 감성 점수 업데이트
│   │   ├── crawl_crypto_dag.py               #1-2 뉴스 크롤링 dag
│   │   ├── crypto_crawler.py                 #1-1 뉴스 크롤링
│   │   ├── gptapi_news_sentiment.py          #2-2 gptapi를 이용한 뉴스 감성 분석
│   │   ├── news_sentiment.py                 #2-1 머신러닝 모델을 이용한 뉴스 감성 분석
│   │   ├── sentiment_analysis_dag.py         #2-3 뉴스 감성분석 dag
│   │   └── update_coin_prospects.py          #4-2 최신 코인 감성 점수 업데이트 dag
│   └── models/
│       └── svm_pipeline_20250401_010208.pkl  #머신러닝 모델 (커스텀SVM)
├── .gitignore                                #Git에 포함되지 않을 파일 설정
├── Dockerfile                                #Airflow Webserver & Scheduler 빌드용 도커파일
├── Jenkinsfile                               #CI/CD 파이프라인 정의
├── docker-compose.build.yml                  #이미지 빌드를 위한 도커 컴포즈 설정 (로컬/CI에서 사용
├── docker-compose.deploy.yml                 #실제 배포용 도커 컴포즈 설정 (서버 배포 시 사용)
├── entrypoint-scheduler.sh                   #Airflow Scheduler 컨테이너의 실행 시작 스크립트
├── entrypoint-webserver.sh                   #Airflow Webserver 컨테이너의 실행 시작 스크립트
├── init.sql                                  #Mysql 초기화용 SQL 스크립트
└── requirements.txt                          #Python 라이브러리 및 패키지 의존성 목록
```

</details>

---
