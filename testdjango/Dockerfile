# Используем официальный Python образ
FROM python:3.12.4

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию
WORKDIR /code

# Устанавливаем зависимости
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код проекта
COPY . /code/
