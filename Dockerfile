FROM python:3.13-slim

WORKDIR /app

# Запобігаємо запису .pyc файлів та буферизації stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Встановлюємо залежності
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо проєкт
COPY . .

# Збираємо статичні файли для WhiteNoise
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Запуск через Gunicorn
CMD ["gunicorn", "shop_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]