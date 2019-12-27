FROM python:3.8-alpine

RUN adduser -D hola

WORKDIR /home/hola

COPY requirements.txt requirements.txt
COPY entrypoint.sh entrypoint.sh
COPY src src

RUN pip install -r requirements.txt && chmod +x entrypoint.sh \
    && chown -R hola:hola ./

USER hola
EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]

