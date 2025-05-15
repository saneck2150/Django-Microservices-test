FROM python:3.12-alpine
WORKDIR /app
COPY ./app.py ./
RUN apk add --no-cache file && \
    pip install fastapi uvicorn[standard] python-magic-bin aiofiles
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]