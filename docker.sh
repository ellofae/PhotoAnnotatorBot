#!/bin/bash

docker build -t bot_image .
docker run -d --name bot_app bot_image
