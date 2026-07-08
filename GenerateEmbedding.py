from flask import Flask, abort, request, jsonify, Response
from sentence_transformers import SentenceTransformer
import numpy as np
import json
import os
import logging

app = Flask(__name__)

MODEL_PATH = os.environ.get("MODEL_PATH", "/models")
MODEL_NAME = os.environ.get("MODEL_NAME", "Qwen/Qwen3-Embedding-0.6B")
DEFAULT_DIMENSION = int(os.environ.get("EMBEDDING_DIMENSION", "1024"))

# Qwen3-Embedding is instruction-aware: queries get an instruction, documents do
# not. The service owns this difference so callers just say "documents" or
# "query". Override the instruction with QUERY_PROMPT.
QUERY_PROMPT = os.environ.get(
    "QUERY_PROMPT",
    "Instruct: Given a user question, retrieve digital repository passages that answer it\nQuery:",
)

model = SentenceTransformer(MODEL_PATH)
NATIVE_DIMENSION = model.get_sentence_embedding_dimension()


def _embed(texts, is_query, dimension):
    """Return a list of normalized float vectors for the given texts."""
    if is_query and QUERY_PROMPT:
        texts = ["{} {}".format(QUERY_PROMPT, t) for t in texts]

    vecs = model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)

    dim = int(dimension) if dimension else DEFAULT_DIMENSION
    if dim and dim < vecs.shape[1]:
        # Matryoshka: truncate then re-normalize so dot_product == cosine.
        vecs = vecs[:, :dim]
        norms = np.linalg.norm(vecs, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        vecs = vecs / norms

    return vecs.tolist()


def _texts_from_request():
    """Extract (texts, dimension) from a JSON body or ?q= for either endpoint."""
    data = request.get_json(silent=True)
    if isinstance(data, dict):
        if isinstance(data.get("texts"), list):
            return [str(t) for t in data["texts"]], data.get("dimension")
        for key in ("text", "q"):
            if key in data:
                return [str(data[key])], data.get("dimension")
    elif isinstance(data, str):
        return [data], None
    q = request.args.get("q")
    if q is not None:
        return [q], None
    return None, None


@app.route("/embed/documents", methods=["POST"])
def embed_documents():
    texts, dimension = _texts_from_request()
    if not texts:
        abort(400)
    embeddings = _embed(texts, is_query=False, dimension=dimension)
    return jsonify(
        {
            "embeddings": embeddings,
            "model": MODEL_NAME,
            "dimension": len(embeddings[0]) if embeddings else 0,
        }
    )


@app.route("/embed/query", methods=["GET", "POST"])
def embed_query():
    texts, dimension = _texts_from_request()
    if not texts:
        abort(400)
    embeddings = _embed(texts, is_query=True, dimension=dimension)
    resp = {
        "embeddings": embeddings,
        "model": MODEL_NAME,
        "dimension": len(embeddings[0]) if embeddings else 0,
    }
    if len(embeddings) == 1:
        # Convenience for single-query callers (e.g. the Go search service).
        resp["embedding"] = embeddings[0]
    return jsonify(resp)


@app.route("/model")
def model_info():
    return jsonify(
        {
            "model": MODEL_NAME,
            "dimension": DEFAULT_DIMENSION,
            "native_dimension": NATIVE_DIMENSION,
            "normalize": True,
        }
    )


@app.route("/", methods=["GET", "POST"])
def generate_embedding():
    """Backwards-compatible single-vector endpoint (document-style)."""
    if request.method == "POST":
        text = request.get_json(silent=True)
    else:
        text = request.args.get("q")
    if not isinstance(text, str):
        abort(400)
    embeddings = _embed([text], is_query=False, dimension=None)
    return Response(json.dumps(embeddings[0]) + "\n", mimetype="application/json")


@app.route("/healthcheck")
def healthcheck():
    return "OK"


@app.errorhandler(404)
def page_not_found(error):
    return "This route does not exist {}".format(request.url), 404


@app.errorhandler(400)
def bad_request(error):
    return 'POST /embed/documents or /embed/query with {"texts": [...]}', 400


class HealthCheckFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("/healthcheck") == -1


# Remove /healthcheck from application server logs.
logging.getLogger("gunicorn.access").addFilter(HealthCheckFilter())

logger = logging.getLogger(__name__)
