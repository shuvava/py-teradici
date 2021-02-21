FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

ARG APP_PORT=80
ARG APP_VERSION=0.0.0.0
EXPOSE $APP_PORT

WORKDIR /app
COPY ./app ./app
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY app/run.sh .
RUN chmod +x run.sh
RUN echo $APP_VERSION > ./app/version.txt

ENV WEBAPP__DEFAULT__CACHE_CONNECTION_STRING=redis
ENV APP_PORT=$APP_PORT

CMD [ "./run.sh" ]
