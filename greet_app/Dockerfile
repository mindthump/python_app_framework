# The base image probably doesn't need to be quite so hefty...
FROM ubuntu:lunar

LABEL Author="github.com/mindthump"
ENV appdir="/app"
ENV TITLE="good person"

WORKDIR ${appdir}

# for my own convenience when ssh-ing to instances
RUN apt-get update -y && apt-get install tmux mc vim less wget pip -y --no-install-recommends

COPY greet_app .
COPY app_utils ./app_utils
COPY tests ./tests

RUN pip install --no-cache-dir --disable-pip-version-check -r requirements.txt
