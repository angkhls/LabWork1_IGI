#!/usr/bin/env bash
set -o errexit

# Установка зависимостей
pip install -r requirements.txt

# Сбор статики
python manage.py collectstatic --no-input

# Применение миграций
python manage.py migrate