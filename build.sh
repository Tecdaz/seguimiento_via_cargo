#!/bin/bash

docker build -t bot-via-cargo .
docker run --name bot-via-cargo --env-file .env --rm bot-via-cargo