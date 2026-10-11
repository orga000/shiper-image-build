FROM python:3.12-alpine

WORKDIR /app

COPY app.py bot.py banner.py requirements.txt index.html ./

EXPOSE 3000

RUN apk update && \
    apk add --no-cache bash curl && \
    apk add --no-cache --virtual .build-deps gcc musl-dev linux-headers && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

CMD ["python3", "app.py"]
