import os
import joblib

from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression


# --------------------------
# Training Data
# --------------------------

simple_prompts = [
    "What is Python?",
    "Capital of India",
    "Who is the president of USA?",
    "Write hello world in Java",
    "What is machine learning?",
    "2 + 2",
    "Define database",
    "What is FastAPI?",
    "What is an API?",
    "Explain recursion briefly",
    "Current weather in Delhi",
    "List Python data types",
    "What is SQL?",
    "What is Docker?",
    "What is Git?"
]

complex_prompts = [
    "Compare FastAPI and Flask in detail.",
    "Design a scalable microservice architecture.",
    "Debug this Python code and explain the issue.",
    "Build an AI chatbot using local LLMs.",
    "Create a system design for log anomaly detection.",
    "Explain transformers step by step.",
    "Implement a recommendation engine using embeddings.",
    "Design a real time chat application architecture.",
    "Analyze the time complexity of this algorithm.",
    "Develop an end to end RAG pipeline.",
    "Explain how distributed databases work.",
    "Create a machine learning pipeline for classification.",
    "Build a secure authentication system.",
    "Research different prompt routing techniques.",
    "Fine tune an LLM on custom data."
]

X = simple_prompts + complex_prompts
y = (
        [0] * len(simple_prompts)
        + [1] * len(complex_prompts)
)

# --------------------------
# Embedding Model
# --------------------------

embedding_model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

embeddings = embedding_model.encode(X)

# --------------------------
# Train Classifier
# --------------------------

classifier = LogisticRegression(
    random_state=42,
    max_iter=1000
)

classifier.fit(
    embeddings,
    y
)

# --------------------------
# Save Model
# --------------------------

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "prompt_classifier.pkl"
)

joblib.dump(
    classifier,
    MODEL_PATH
)

print("Classifier saved to:")
print(MODEL_PATH)