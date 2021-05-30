FROM python:3.9-slim
RUN apt-get update && apt-get upgrade -y
RUN adduser --system --group --no-create-home app
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN chown -R app:app /app