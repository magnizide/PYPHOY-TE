ARG IMAGE_VERSION=3.12
FROM python:${IMAGE_VERSION}

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' && \
    apt-get update && apt-get -y install google-chrome-stable && \
    pip install pipenv && \
    useradd -ms /bin/bash pyphoy

USER pyphoy
COPY . /opt/app
WORKDIR /opt/app

RUN pipenv install

ENTRYPOINT [ "pipenv", "run", "python", "src/bot.py" ]