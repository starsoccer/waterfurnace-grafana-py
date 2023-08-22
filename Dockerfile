FROM python:slim
WORKDIR /app

COPY . .

CMD [ "python3",  "index.py" ]