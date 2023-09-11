FROM python:bookworm

LABEL Author="github.com/mindthump"
ENV appdir="/app"

WORKDIR ${appdir}

# for my own convenience when ssh-ing to instances
RUN apt update && \
  DEBIAN_FRONTEND=noninteractive apt install --yes --quiet --autoremove --no-install-suggests --no-install-recommends \
  jq mc neovim httpie pip bat iproute2 nmap \
  && apt clean && rm -rf /var/lib/apt/lists/*

COPY fruit_server_app ./fruit_server_app
COPY app_utils ./app_utils
RUN chown -R "$UID:$GID" .

RUN pip install --no-cache-dir --disable-pip-version-check -r fruit_server_app/requirements.txt
