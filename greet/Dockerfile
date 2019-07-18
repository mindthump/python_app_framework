FROM python:3.7-alpine

LABEL Author="github.com/mindthump"
ENV appdir="/usr/src/app"
ENV TITLE="good person"

# ... no ports needed (yet)
# EXPOSE 5000

WORKDIR ${appdir}

# for my own convenience when ssh-ing to instances
RUN apk add curl byobu mc vim

COPY . .

RUN pip install --no-cache-dir --disable-pip-version-check -r requirements.txt

ENTRYPOINT ["python3", "greet.py"]

# Override default ('Hola!')
CMD ["--greeting", "Howdy!"]
