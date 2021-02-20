#! /usr/bin/env bash
# set variables
: "${APP_PORT:=80}"
echo "app version $(cat ./app/version.txt)"
uvicorn 'app.run:app' --host "0.0.0.0" --port $APP_PORT
