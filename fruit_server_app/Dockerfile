FROM python:3.7

LABEL Author="github.com/mindthump"
ENV appdir="/app"
ENV TITLE="good person"

EXPOSE 8000

WORKDIR ${appdir}

# for my own convenience when ssh-ing to instances
RUN apt-get update -y && apt-get install tmux mc vim httpie less -y --no-install-recommends

# NOTE: You could copy everything to the image, but I just bind-mount the app dir in compose
COPY requirements.txt .

RUN pip install --no-cache-dir --disable-pip-version-check -r requirements.txt


