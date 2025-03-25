from flask import Flask, abort, request
from sentence_transformers import SentenceTransformer
import json
import os

app = Flask(__name__)

MODEL_PATH = os.environ.get("MODEL_PATH", "/app/sbert/models")
model = SentenceTransformer(MODEL_PATH)


@app.errorhandler(404)
def page_not_found(error):
    return "This route does not exist {}".format(request.url), 404


@app.errorhandler(400)
def bad_request(error):
    return "Valid routes are only /?q=SENTENCE", 400


@app.route("/")
def generate_embedding():
    text = request.args.get("q")
    if text is None:
        abort(400)
    embeddings = model.encode(text)
    embeddingsJson = json.dumps(embeddings.tolist()) + "\n"
    return embeddingsJson
