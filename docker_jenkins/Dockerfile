# ✅ Ubuntu 22.04 기반 Python 3.10 사용
FROM ubuntu:22.04

USER root

# ✅ airflow 사용자 먼저 생성
RUN useradd -m airflow

# 시스템 패키지 + Chrome 설치
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

# Airflow 디렉토리 권한 설정
RUN mkdir -p /opt/airflow && chown -R airflow:airflow /opt/airflow

# airflow 사용자 전환
USER airflow
ENV HOME=/home/airflow

WORKDIR /opt/airflow

# requirements 복사 및 설치
COPY requirements.txt .
RUN python3.10 -m venv /opt/airflow/venv && \
    /opt/airflow/venv/bin/pip install --upgrade pip && \
    /opt/airflow/venv/bin/pip install apache-airflow==2.7.2 && \
    /opt/airflow/venv/bin/pip install --no-cache-dir -r requirements.txt

# DAG, model, 초기 SQL 복사
COPY ./airflow/dags /opt/airflow/dags
COPY ./airflow/models /opt/airflow/models
COPY init.sql /opt/airflow/init.sql

# entrypoint 스크립트 복사 및 실행 권한 부여
COPY --chown=airflow:airflow entrypoint-webserver.sh /entrypoint-webserver.sh
COPY --chown=airflow:airflow entrypoint-scheduler.sh /entrypoint-scheduler.sh
RUN chmod +x /entrypoint-webserver.sh /entrypoint-scheduler.sh

# airflow 기본 환경
ENV PATH="/opt/airflow/venv/bin:$PATH"
ENV AIRFLOW_HOME="/opt/airflow"

# 포트 노출
EXPOSE 8080
