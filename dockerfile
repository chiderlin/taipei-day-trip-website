# FROM python:3.8.1
FROM ubuntu:18.04
MAINTAINER Chi Lin "chiderlin36@gmail.com"
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    python3.8 python3-pip python3.8-dev
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 3000
CMD ["python3", "app.py"]