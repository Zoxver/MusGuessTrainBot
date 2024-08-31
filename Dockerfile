# Используем официальный образ Python 3.10 в качестве базового образа
FROM python:3.10-slim

# Устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    cmake \
    make \
    g++ \
    zlib1g-dev \
    libssl-dev \
    gperf \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Клонируем репозиторий и собираем telegram-bot-api
RUN git clone --recursive https://github.com/tdlib/telegram-bot-api.git && \
    cd telegram-bot-api && \
    rm -rf build && \
    mkdir build && \
    cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX:PATH=.. .. && \
    cmake --build . --target install

# Копируем текущую директорию в контейнер
COPY . /app

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с переменными окружения
COPY .env /app/.env

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Запускаем сервер telegram-bot-api и бота
CMD ["sh", "-c", "/telegram-bot-api/bin/telegram-bot-api --local --api-id=$API_ID --api-hash=$API_HASH --log=/var/log/telegram-bot-api.log & python bot.py"]
