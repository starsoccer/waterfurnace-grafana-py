FROM telegraf:alpine

COPY requirements.txt requirements.txt
COPY index.py index.py
COPY start.sh start.sh

RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

RUN ls
RUN pip install prometheus-client
RUN pip3 install prometheus_client
RUN pip3 install waterfurnace

RUN ["chmod", "+x", "start.sh"]

CMD [ "./start.sh" ]