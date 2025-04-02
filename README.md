# AI-repo
### 📁 AI-repo 구조

<details>
<summary><strong>📂 docker-jenkins 구조</strong></summary>

```
docker-jenkins/
├── airflow/
│   ├── dags/
│   │   ├── coin_sentiment_stats.py   
│   │   ├── coin_stats_dag.py
│   │   ├── coin_update.py
│   │   ├── crawl_crypto_dag.py
│   │   ├── crypto_crawler.py
│   │   ├── gptapi_news_sentiment.py
│   │   ├── news_sentiment.py
│   │   ├── sentiment_analysis_dag.py
│   │   └── update_coin_prospects.py
│   └── models/
│       └── svm_pipeline_20250401_010208.pkl
├── .gitignore
├── Dockerfile
├── Jenkinsfile
├── docker-compose.build.yml
├── docker-compose.deploy.yml
├── entrypoint-scheduler.sh
├── entrypoint-webserver.sh
├── init.sql
├── requirements.txt
└── README.md
```

</details>

---
