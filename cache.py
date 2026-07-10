from sentence_transformers import SentenceTransformer
import os

MODEL_PATH = os.environ.get("MODEL_PATH", "/models")
MODEL_NAME = os.environ.get("MODEL_NAME", "Qwen/Qwen3-Embedding-0.6B")
TOKENIZER_KWARGS = {"fix_mistral_regex": True}

# Downloaded and baked into the image at build time. To change the model, set
# MODEL_NAME (and keep EMBEDDING_DIMENSION and the Solr DenseVectorField in sync).
model = SentenceTransformer(MODEL_NAME, tokenizer_kwargs=TOKENIZER_KWARGS)
model.save(MODEL_PATH)
