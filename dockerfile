FROM python:3.8.1
MAINTAINER Chi Lin "chiderlin36@gmail.com"
COPY ./app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 3000
CMD ["python", "app.py"]