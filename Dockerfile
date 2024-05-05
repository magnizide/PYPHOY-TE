# Build for AMD64
ARG IMAGE_VERSION=3.10-alpine
FROM python:${IMAGE_VERSION}

ARG APP_DIR=/opt/app
COPY --chown=pyphoy:pyphoy . ${APP_DIR}
RUN apk add --no-cache chromium gcompat && \
    pip install --no-cache-dir -r ${APP_DIR}/src/requirements.txt && \
    adduser -Ds /bin/bash pyphoy

USER pyphoy

WORKDIR ${APP_DIR}

ENTRYPOINT [ "python", "src/bot.py" ]