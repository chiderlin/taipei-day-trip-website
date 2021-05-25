# FROM python:3.8.1
FROM ubuntu:latest
MAINTAINER Chi Lin "chiderlin36@gmail.com"
RUN apt-get update && \
    # 不要出現互動訊息
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata && \ 
    apt-get install -y vim && \
    apt-get install --no-install-recommends -y && \
    python3.8 python3-pip python3.8-dev
RUN TZ=Asia/Taipei \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata 

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 3000
CMD ["python3", "app.py"]