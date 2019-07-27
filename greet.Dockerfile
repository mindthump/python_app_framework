FROM python:3.7

LABEL Author="github.com/mindthump"
ENV appdir="/app"
ENV TITLE="good person"

WORKDIR ${appdir}

# for my own convenience when ssh-ing to instances
RUN apt-get update -y && apt-get install tmux mc vim httpie less -y --no-install-recommends

COPY greet_app .
COPY toolbox ./toolbox

RUN pip install --no-cache-dir --disable-pip-version-check -r requirements.txt