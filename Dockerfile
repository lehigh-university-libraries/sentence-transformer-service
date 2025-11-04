FROM ghcr.io/lehigh-university-libraries/python3.13:main@sha256:46731c8d3efc11d8748996be972b8a163571acf5a84a714efde5ad92b0cefbc6

COPY requirements.txt /app
RUN uv pip install \
   --break-system-packages \
   --system \
   -r /app/requirements.txt

COPY cache.py /app

ENV FLASK_APP="GenerateEmbedding:app" \
    MODEL_PATH=/models

# cache the model in the docker image
RUN python3 /app/cache.py && ls -l /models/model.safetensors

COPY . /app
