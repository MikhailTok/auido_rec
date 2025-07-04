# # Используем официальный образ Python
# FROM python:3.8

# # Устанавливаем FFmpeg
# RUN apt-get update && apt-get install -y ffmpeg

# # Устанавливаем рабочую директорию
# WORKDIR /app

# # Копируем файлы приложения в контейнер
# COPY . /app

# # Устанавливаем зависимости
# RUN pip install -r requirements.txt

# # Указываем порт, который будет слушать приложение
# EXPOSE 5000

# # Команда для запуска приложения
# CMD ["python", "audio.py"]


FROM python:3.12
# Устанавливаем FFmpeg
RUN apt-get update && apt-get install -y ffmpeg
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["audio.py"]
EXPOSE 5000