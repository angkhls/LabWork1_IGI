#!/usr/bin/env bash
# Выход при любой ошибке
set -o errexit

# 1. Устанавливаем все зависимости (это критически важно!)
pip install -r requirements.txt

# 2. Применяем миграции
python manage.py migrate --noinput

# 3. Собираем статику
python manage.py collectstatic --noinput