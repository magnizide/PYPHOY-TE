FROM python:3.12

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' && \
    apt-get update && apt-get -y install google-chrome-stable && \
    pip install pipenv && \
    useradd -ms /bin/bash pyphoy

RUN pipenv install --dev

USER pyphoy 
WORKDIR /opt/app
