FROM python:3

RUN pip3 install --upgrade pip3 && \
    pip3 install --no--cache-dir mysqlclient

ADD server.py /

EXPOSE 9010

CMD [ "python", "./server.py" ]
