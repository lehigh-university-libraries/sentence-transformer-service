FROM ghcr.io/lehigh-university-libraries/python3.13:main

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
