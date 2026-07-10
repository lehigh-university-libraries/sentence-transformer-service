FROM ghcr.io/lehigh-university-libraries/python3.13:main@sha256:46731c8d3efc11d8748996be972b8a163571acf5a84a714efde5ad92b0cefbc6

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
    MODEL_PATH=/models \
    MODEL_NAME="Qwen/Qwen3-Embedding-0.6B" \
    EMBEDDING_DIMENSION=1024

# cache the model in the docker image
RUN python3 /app/cache.py && python3 -c "from sentence_transformers import SentenceTransformer; m = SentenceTransformer('/models'); print(m.get_sentence_embedding_dimension())"

COPY . /app

EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--timeout", "600", "GenerateEmbedding:app"]
