from flask import Flask, request
from sentence_transformers import SentenceTransformer
import json

# import time

app = Flask(__name__)

MODEL_PATH = '/opt/sbert/models'
# model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
# model.save(MODEL_PATH)

model = SentenceTransformer(MODEL_PATH)

@app.route("/generate-embedding")
def generate_embedding():
    text = request.args.get('q')

    # return "<p>Hello " + text + "!</p>\n"

    # start = time.time()
    embeddings = model.encode(text)
    # end = time.time()
    # print (end - start)
    embeddingsJson = json.dumps(embeddings.tolist()) + '\n'
    return embeddingsJson
