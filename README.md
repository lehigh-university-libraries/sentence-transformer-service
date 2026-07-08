# sentence-transformer-service

Web service to generate embeddings via a Sentence Transformers model.

Model: **Qwen/Qwen3-Embedding-0.6B** (1024-d, normalized). Used by
`islandora_rag` (Drupal indexing) and the Go `search` service (query time) for
semantic / RAG search. See `docs/islandora_rag.md`.

## API

- `POST /embed/documents` — embed passages (no instruction).
  Body: `{"texts": ["..."], "dimension": 1024}` → `{"embeddings": [[...]], "model", "dimension"}`
- `POST /embed/query` — embed a user question (Qwen3 query instruction applied).
  Body: `{"texts": ["..."]}` or `{"text": "..."}` → `{"embeddings": [[...]], "embedding": [...]}`
- `GET /model` — `{"model", "dimension", "native_dimension", "normalize"}`
- `GET /healthcheck` — `OK`
- `GET|POST /` — legacy single-vector endpoint (document-style).

Vectors are L2-normalized (so Solr `dot_product` == cosine). `dimension` may be
any value ≤ native (1024) — Qwen3 is Matryoshka-trained, so we truncate and
re-normalize. Keep `dimension` in sync with the Solr `DenseVectorField`.

```
curl -H "Content-Type: application/json" \
  -d '{"texts": ["Please excuse my dear aunt sally!"]}' \
  http://embed:8080/embed/documents
```

Config (env): `MODEL_NAME` (default `Qwen/Qwen3-Embedding-0.6B`),
`EMBEDDING_DIMENSION` (default `1024`), `QUERY_PROMPT` (query instruction),
`MODEL_PATH` (baked-in model dir).

`QUERY_PROMPT` is model-specific. If `MODEL_NAME` changes, review the query
instruction at the same time; using a prompt tuned for a different embedding
model can silently degrade retrieval quality.

## Developing locally

You can build the service via

```
docker build -t ghcr.io/lehigh-university-libraries/sentence-transformer:main .
```

Then make it available on your local machine with

```
docker run -p 8080:8080 ghcr.io/lehigh-university-libraries/sentence-transformer:main
```

Then open [http://localhost:8080/?q=foo+bar+baz](http://localhost:8080/?q=foo+bar+baz) in your web browser to see the embeddings for the sentence `foo bar baz`

## Updating model

The model is cached when the docker image is built with the script [cache.py](./cache.py)

So if we ever want to update the model this service uses, or update the model, we can modify that script accordingly.

## Attribution

Initial implementation inspired by https://github.com/jcoyne/code4lib-2024-ai-workshop
