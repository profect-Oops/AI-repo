# ✅ Ubuntu 22.04 기반 Python 3.10 사용
FROM ubuntu:22.04

# ✅ 루트 권한으로 시스템 패키지 설치
USER root

# 필수 패키지 설치 및 Chrome 설치
RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    curl \
    unzip \
    libnss3 \
    libxss1 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libgdk-pixbuf2.0-0 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libnspr4 \
    libx11-xcb1 \
    libxtst6 \
    libxkbcommon0 \
    ca-certificates \
    fonts-liberation \
    libxshmfence1 \
    xdg-utils \
    pkg-config \
    libmysqlclient-dev \
    mysql-client \
    python3.10 \
    python3.10-venv \
    python3.10-dev \
    python3-pip && \
    wget https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.117/linux64/chrome-linux64.zip && \
    unzip chrome-linux64.zip && \
    mv chrome-linux64 /opt/chrome && \
    ln -s /opt/chrome/chrome /usr/bin/google-chrome && \
    rm chrome-linux64.zip && \
    wget https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.117/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    chmod +x chromedriver-linux64/chromedriver && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \ 
    mkdir -p /opt/airflow/bin && \
    cp /usr/local/bin/chromedriver /opt/airflow/bin/chromedriver && \
    chown airflow:airflow /opt/airflow/bin/chromedriver && \
    chmod +x /opt/airflow/bin/chromedriver && \
    rm -rf chromedriver-linux64 chromedriver-linux64.zip &&\
    rm -rf /var/lib/apt/lists/*

# ✅ Airflow 사용자 추가 (Ubuntu 기본 계정 X)
RUN mkdir -p /opt/airflow && chown -R airflow:airflow /opt/airflow

# ✅ airflow 사용자로 변경 (venv 생성 전에 변경)
USER airflow
ENV HOME=/home/airflow

# ✅ airflow 사용자의 홈 디렉토리 설정
WORKDIR /opt/airflow

# ✅ requirements.txt 복사
COPY requirements.txt .

# ✅ airflow 사용자 환경에서 venv 생성 및 pip 설치
RUN python3.10 -m venv /opt/airflow/venv && \
    /opt/airflow/venv/bin/pip install --upgrade pip && \
    /opt/airflow/venv/bin/pip install apache-airflow==2.7.2

# ✅ requirements.txt 복사
COPY requirements.txt .

# ✅ requirements.txt 설치 (이제 Airflow가 정상적으로 설치된 상태에서 실행됨)
RUN /opt/airflow/venv/bin/pip install --no-cache-dir -r requirements.txt

# DAG 복사
COPY ./airflow/dags /opt/airflow/dags

# ✅ MySQL 테이블 자동 생성 SQL 복사
COPY init.sql /opt/airflow/init.sql

# ✅ Webserver & Scheduler 엔트리포인트 추가 (root에서 복사 & 권한 설정)
COPY --chown=airflow:airflow entrypoint-webserver.sh /entrypoint-webserver.sh
COPY --chown=airflow:airflow entrypoint-scheduler.sh /entrypoint-scheduler.sh
RUN chmod +x /entrypoint-webserver.sh /entrypoint-scheduler.sh

# ✅ airflow 사용자로 변경 (이제 변경!)
USER airflow
ENV HOME=/home/airflow

# ✅ Airflow 명령어 실행 가능하도록 PATH 설정
ENV PATH="/opt/airflow/venv/bin:$PATH"
ENV AIRFLOW_HOME="/opt/airflow"

# ✅ 환경 변수 설정 (MySQL & API 키)
ENV AIRFLOW_HOME=/opt/airflow
ENV DB_HOST=oops-mysql-db.cjw2u00m0szc.ap-northeast-2.rds.amazonaws.com
ENV DB_PORT=3306
ENV DB_USER=oops_team
ENV DB_NAME=oops

# 포트 오픈
EXPOSE 8080
