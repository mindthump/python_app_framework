# Base image with tools for my own convenience when ssh-ing to instances
FROM python:3.9 as appbase
LABEL Author="github.com/mindthump"
COPY requirements.txt .
RUN apt-get update -y && apt-get install tmux mc vim httpie less -y --no-install-recommends
RUN pip3 install --no-cache-dir --disable-pip-version-check -r requirements.txt && rm requirements.txt

# Fruit
FROM appbase as fruit_server
ENV TITLE="good person"
EXPOSE 8000
WORKDIR /app
COPY fruit_server_app/* ./
COPY toolbox ./toolbox

# Greet
FROM appbase as greet_server
ENV TITLE="good person"
WORKDIR /app
COPY greet_app/* ./
COPY toolbox ./toolbox
