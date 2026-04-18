#!/bin/sh

echo "⏳ Waiting for database..."
sleep 2

echo "🔄 Running migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "📦 Loading demo data..."
python setup_demo.py

echo "🚀 Starting server..."
exec python manage.py runserver 0.0.0.0:8000
