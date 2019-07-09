FROM python:3.7.0-alpine3.8

LABEL Author="github.com/mindthump"
ENV appdir="/usr/src/app"
ENV TITLE="good person"

# ... no ports needed (yet)
# EXPOSE 5000

WORKDIR ${appdir}

# for my own convenience when ssh-ing to instances
RUN apk add curl
RUN apk add zsh
# RUN apk add byobu

COPY . .

RUN pip install --no-cache-dir --disable-pip-version-check -r requirements.txt

CMD python ${appdir}/sample_app.py --greeting "Salutations"
