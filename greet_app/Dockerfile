FROM python:bookworm

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# for my own convenience when ssh-ing to instances
RUN apt-get update -y && apt-get install jq mc vim httpie less pip bat iproute2 nmap -y --no-install-recommends

COPY greet_app .
COPY app_utils ./app_utils

RUN pip install -r requirements.txt

CMD ["bash"]
