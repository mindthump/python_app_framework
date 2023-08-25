FROM python:3.9-alpine

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY greet_app .
COPY app_utils ./app_utils

RUN pip install -r requirements.txt

CMD ["ash"]
