from sentence_transformers import SentenceTransformer
import os

MODEL_PATH = os.environ.get("MODEL_PATH", "/app/models")

model = SentenceTransformer(
    model_name_or_path="sentence-transformers/all-MiniLM-L6-v2",
    revision="c9745ed1d9f207416be6d2e6f8de32d1f16199bf",
)

model.save(MODEL_PATH)
