#!/bin/bash

echo "Waiting for MySQL to be ready..."
until mysqladmin ping -h "$DB_HOST" --silent; do
    echo "MySQL is unavailable - sleeping"
    sleep 5
done

echo "Checking if target tables exist in '$DB_NAME'..."
TABLE_COUNT=$(mysql -h $DB_HOST -P $DB_PORT -u $DB_USER -p$DB_PASSWORD -N -e "
  SELECT COUNT(*) FROM information_schema.TABLES
  WHERE TABLE_SCHEMA = '$DB_NAME'
  AND (TABLE_NAME = 'news_sentiment' OR TABLE_NAME = 'coin_sentiment_stats');
")

if [ "$TABLE_COUNT" -eq 0 ]; then
  echo "🛠 Setting up schema from setup_schema.sql..."
  mysql -h $DB_HOST -P $DB_PORT -u $DB_USER -p$DB_PASSWORD $DB_NAME < /opt/airflow/setup_schema.sql
else
  echo "✅ Tables already exist. Skipping schema setup."
fi
