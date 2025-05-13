# official minimal python
FROM python:3.12-slim

# Working directory
WORKDIR /app

# copying dependencies
COPY requirements.txt .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .

# open port
EXPOSE 8080

# run command
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8080"]
