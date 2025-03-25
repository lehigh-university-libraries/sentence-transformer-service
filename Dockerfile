FROM python:3.13-bookworm@sha256:ae9f9ac89467077ed1efefb6d9042132d28134ba201b2820227d46c9effd3174

WORKDIR /app

# renovate: datasource=repology depName=debian_12/gosu
ARG GOSU_VERSION="1.14-1+b10"
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    gosu="${GOSU_VERSION}" \
  && rm -rf /var/lib/apt/lists/* \
  && groupadd -r nobody \
  && useradd -r -g nobody transformer \
  && chown transformer /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY cache.py /app

ENV FLASK_APP=GenerateEmbedding \
    MODEL_PATH=/app/models \
    ADDRESS=0.0.0.0 \
    PORT=8080 \
    WORKERS=4

# cache the model in the docker image
RUN python /app/cache.py && ls -l /app/models/model.safetensors

COPY . /app

ENTRYPOINT ["/app/docker-entrypoint.sh"]
