# FROM python:3.8.1
FROM ubuntu:16.04
MAINTAINER Chi Lin "chiderlin36@gmail.com"
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 3000
CMD ["python", "app.py"]