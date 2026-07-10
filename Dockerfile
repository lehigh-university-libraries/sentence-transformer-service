FROM ghcr.io/lehigh-university-libraries/python3.13:main@sha256:90ea476591cd5f617744dbd08d4152504300c96cc17deefc158037a9c4e14790

COPY requirements.txt /app
RUN uv pip install \
   --break-system-packages \
   --system \
   -r /app/requirements.txt

COPY cache.py /app

ENV FLASK_APP="GenerateEmbedding:app" \
    HOME=/tmp \
    XDG_CACHE_HOME=/tmp/.cache \
    GUNICORN_CMD_ARGS="--worker-tmp-dir /tmp --chdir /app" \
    WORKERS=1 \
    MODEL_PATH=/models \
    MODEL_NAME="Qwen/Qwen3-Embedding-0.6B" \
    EMBEDDING_DIMENSION=1024

# cache the model in the docker image and verify the runtime user can load it
RUN python3 /app/cache.py \
    && python3 -c "from sentence_transformers import SentenceTransformer; m = SentenceTransformer('/models', processor_kwargs={'fix_mistral_regex': True}); print(m.get_embedding_dimension())" \
    && chown -R pyapp:pyapp /models \
    && s6-setuidgid pyapp python3 -c "from sentence_transformers import SentenceTransformer; m = SentenceTransformer('/models', processor_kwargs={'fix_mistral_regex': True}); print(m.get_embedding_dimension())"

COPY . /app

EXPOSE 8080
HEALTHCHECK CMD curl -f http://localhost:8080/healthcheck || exit 1
