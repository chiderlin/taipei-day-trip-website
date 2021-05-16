# FROM python:3.8.1
FROM ubuntu:latest
MAINTAINER Chi Lin "chiderlin36@gmail.com"
RUN apt-get update && \
    apt-get install -y vim && \
    apt-get install --no-install-recommends -y \
    python3.8.1 python3-pip python3.8-dev
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 3000
CMD ["python3", "app.py"]