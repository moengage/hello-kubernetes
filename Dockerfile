FROM python:3.8-alpine

RUN adduser -D hello

WORKDIR /home/hello

COPY requirements.txt requirements.txt
COPY entrypoint.sh entrypoint.sh
COPY src src

RUN pip install -r requirements.txt && chmod +x entrypoint.sh \
    && chown -R hello:hello ./

USER hello
EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]

