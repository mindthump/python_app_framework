FROM python:3.9

LABEL Author="github.com/mindthump"
ENV appdir="/app"

EXPOSE 8000

WORKDIR ${appdir}

# for my own convenience when ssh-ing to instances
RUN apt-get update -y && apt-get install tmux mc vim httpie less pip -y --no-install-recommends

COPY fruit_server_app ./fruit_server_app
COPY tests ./tests
COPY app_utils ./app_utils
RUN chown -R "$UID:$GID" . /data

RUN pip install --no-cache-dir --disable-pip-version-check -r fruit_server_app/requirements.txt
