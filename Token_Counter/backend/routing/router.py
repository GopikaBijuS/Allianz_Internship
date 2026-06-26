import os
import joblib
from sentence_transformers import SentenceTransformer


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "prompt_classifier.pkl"
)

classifier = joblib.load(MODEL_PATH)

embedding_model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)


def classify_prompt(prompt: str):

    embedding = embedding_model.encode(
        [prompt]
    )

    prediction = classifier.predict(
        embedding
    )[0]

    if prediction == 0:
        return "simple"

    return "complex"


def route_model(prompt: str):

    prompt_type = classify_prompt(prompt)

    if prompt_type == "simple":
        model = "qwen2.5:3b"
    else:
        model = "mistral:7b"

    return model, prompt_type