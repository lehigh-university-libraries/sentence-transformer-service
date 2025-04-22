FROM python:3.13-bookworm@sha256:07bf1bd38e191e3ed18b5f3eb0006d5ab260cb8c967f49d3bf947e5c2e44d8a9

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

HEALTHCHECK CMD curl -f http://localhost:$PORT/healthcheck
