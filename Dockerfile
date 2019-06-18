FROM python:3.7.0-alpine3.8

LABEL Author="github.com/mindthump"
ENV appdir="/usr/src/app"

# ... no ports needed (yet)
# EXPOSE 5000

WORKDIR ${appdir}

COPY requirements.txt ${appdir}/requirements.txt
RUN pip install -r requirements.txt

COPY . ${appdir}

CMD python ${appdir}/sample_app.py
