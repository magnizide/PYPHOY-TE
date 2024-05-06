# Build for AMD64
ARG IMAGE_VERSION=3.10-alpine
FROM python:${IMAGE_VERSION} AS builder

ENV PIPENV_VENV_IN_PROJECT=1

ADD . /usr/app/

WORKDIR /usr/app

RUN pip install --no-cache-dir pipenv==2023.12.1 && \
    pipenv update && \
    pipenv requirements | tee src/requirements.txt

FROM python:${IMAGE_VERSION} AS runtime

ARG APP_DIR=/opt/app

COPY --from=builder /usr/app/src/ ${APP_DIR}/src/

WORKDIR ${APP_DIR}

RUN apk add --no-cache chromium gcompat && \
    pip install --no-cache-dir -r ${APP_DIR}/src/requirements.txt && \
    adduser -Ds /bin/bash pyphoy

USER pyphoy
ENTRYPOINT [ "python", "src/bot.py" ]