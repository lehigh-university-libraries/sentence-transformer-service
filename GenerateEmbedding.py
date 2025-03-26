from flask import Flask, abort, request, Response
from sentence_transformers import SentenceTransformer
import json
import os
import logging

app = Flask(__name__)

MODEL_PATH = os.environ.get("MODEL_PATH", "/app/models")
model = SentenceTransformer(MODEL_PATH)


@app.errorhandler(404)
def page_not_found(error):
    return "This route does not exist {}".format(request.url), 404


@app.errorhandler(400)
def bad_request(error):
    return "Valid routes are only GET /?q=SENTENCE and POST /", 400


@app.route("/", methods=["GET", "POST"])
def generate_embedding():
    if request.method == "POST":
        text = request.get_json()
    else:
        text = request.args.get("q")

    if type(text) is not str:
        abort(400)

    embeddings = model.encode(text)
    embeddingsJson = json.dumps(embeddings.tolist()) + "\n"
    return Response(embeddingsJson, mimetype="application/json")


@app.route("/healthcheck")
def healthcheck():
    return "OK"


class HealthCheckFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("/healthcheck") == -1


# Remove /healthcheck from application server logs
logging.getLogger("gunicorn.access").addFilter(HealthCheckFilter())

logger = logging.getLogger(__name__)
