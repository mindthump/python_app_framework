FROM python:bookworm

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

LABEL Author="github.com/mindthump"
ENV appdir="/app"

WORKDIR ${appdir}

# for my own convenience when ssh-ing to instances
RUN apt update && \
  DEBIAN_FRONTEND=noninteractive apt install --yes --quiet --autoremove --no-install-suggests --no-install-recommends \
  jq mc neovim httpie pip bat iproute2 nmap \
  && apt clean && rm -rf /var/lib/apt/lists/*

COPY greet_app .
COPY app_utils ./app_utils

RUN pip install -r requirements.txt

CMD ["bash"]
