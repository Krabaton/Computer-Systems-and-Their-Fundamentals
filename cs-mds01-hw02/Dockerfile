FROM python:3.11-slim

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY . .

RUN pip install -r requirements.txt

EXPOSE 3000

CMD ["python", "main.py"]