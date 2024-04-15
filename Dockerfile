FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE $PORT
CMD [ "python3", "gunicorn --workers=4 --bind 0.0.0.0:$PORT app:app"]