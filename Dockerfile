FROM python:3.11

# Встановлюємо pdflatex
RUN apt-get update && \
    apt-get install -y texlive-base texlive-fonts-recommended && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

# Встановлюємо всі залежності
RUN pip install --no-cache-dir -r requirements.txt

# Відкриваємо порт 8000 для сервера Gunicorn
EXPOSE 8000

CMD ["gunicorn", "kursova.wsgi:application", "--bind", "0.0.0.0:8000"]