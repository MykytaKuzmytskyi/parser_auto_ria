FROM python:3.10.8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
RUN apt-get update && apt-get install -y xvfb chromium
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/