FROM python:3.9

LABEL Author="github.com/mindthump"
ENV appdir="/app"
ENV TITLE="good person"

EXPOSE 8000

WORKDIR ${appdir}

# for my own convenience when ssh-ing to instances
RUN apt-get update -y && apt-get install tmux mc vim httpie less pip -y --no-install-recommends

COPY fruit_server_app .
COPY toolbox ./toolbox
COPY tests ./tests
COPY conftest.py .

RUN pip install --no-cache-dir --disable-pip-version-check -r requirements.txt
