FROM python:bookworm

LABEL Author="github.com/mindthump"
ENV appdir="/app"

WORKDIR ${appdir}

# for my own convenience when ssh-ing to instances
RUN apt-get update -y && apt-get install jq mc vim httpie less pip bat -y --no-install-recommends

COPY fruit_server_app ./fruit_server_app
COPY app_utils ./app_utils
RUN chown -R "$UID:$GID" .

RUN pip install --no-cache-dir --disable-pip-version-check -r fruit_server_app/requirements.txt
