FROM python:3.8


RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip python3-venv python3-dev git && \
    pip install --no-cache --upgrade pip  && \
    pip install poetry==1.3.1
# Создание и установка рабочего каталога
WORKDIR /app

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости с использованием Poetry
RUN poetry install

# Запускаем команду при запуске контейнера
CMD ["poetry", "run", "python", "src/main.py"]
