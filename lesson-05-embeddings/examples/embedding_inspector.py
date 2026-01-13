import os
from pathlib import Path
from typing import List, Tuple

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI


SENTENCES: List[str] = [
    "Ransomware encrypts systems and prevents access to critical data.",
    "Recovering data after a malware-driven encryption event is a core part of incident response.",
    "What's the weather forecast for tomorrow in Toronto?",
    "Backups are only useful if you regularly test restores and verify you can recover cleanly.",
]
SENTENCES: List[str] = [
    "The concert was cancelled due to rain",
    "Severe weather forced the event to be called off",
    "I saw the man through the telescope.",
    "I saw the man who had a telescope.",
]

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity: 1.0 = very similar direction, 0.0 = unrelated."""
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def get_embeddings(client: OpenAI, texts: List[str], model: str) -> np.ndarray:
    """
    Create embeddings for a list of strings.
    Returns a numpy array shaped (len(texts), embedding_dim).
    """
    resp = client.embeddings.create(model=model, input=texts)
    vectors = [item.embedding for item in resp.data]
    return np.array(vectors, dtype=np.float32)


def preview_vector(vec: np.ndarray, n: int = 10) -> str:
    """Pretty preview of first N values."""
    shown = ", ".join(f"{x:.3f}" for x in vec[:n])
    return f"[{shown}, ...]"


def main() -> None:
    # Load .env from the same directory as this script (robust)
    env_path = Path(__file__).parent / ".env"
    load_dotenv(dotenv_path=env_path, override=True)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            f"OPENAI_API_KEY not found. Create {env_path} based on .env.example."
        )

    client = OpenAI(api_key=api_key)

    # Good default for demos: fast + inexpensive
    embedding_model = "text-embedding-3-small"

    print("\n=== Sentences ===")
    for i, s in enumerate(SENTENCES, start=1):
        print(f"{i}. {s}")

    # 1) Generate embeddings
    vectors = get_embeddings(client, SENTENCES, model=embedding_model)
    dim = vectors.shape[1]

    print("\n=== Embedding Details ===")
    print(f"Embedding model: {embedding_model}")
    print(f"Number of embeddings: {len(SENTENCES)}")
    print(f"Embedding dimension: {dim}")

    # 2) Show preview of each embedding
    for i, s in enumerate(SENTENCES, start=1):
        v = vectors[i - 1]
        print(f"\nSentence {i}: {s}")
        print(f"Vector preview (first 10 values): {preview_vector(v, n=10)}")

    # 3) Similarity matrix
    print("\n=== Cosine Similarity Matrix ===")
    # Compute pairwise cosine similarity
    sim = np.zeros((len(SENTENCES), len(SENTENCES)), dtype=np.float32)
    for i in range(len(SENTENCES)):
        for j in range(len(SENTENCES)):
            sim[i, j] = cosine_similarity(vectors[i], vectors[j])

    # Print header
    header = "      " + "  ".join(f"{i+1:>6}" for i in range(len(SENTENCES)))
    print(header)
    for i in range(len(SENTENCES)):
        row = "  ".join(f"{sim[i, j]:6.3f}" for j in range(len(SENTENCES)))
        print(f"{i+1:>4}  {row}")

    # 4) For each sentence, show the closest other sentence
    print("\n=== Closest Match For Each Sentence ===")
    for i in range(len(SENTENCES)):
        # ignore self by setting it to -inf
        scores = sim[i].copy()
        scores[i] = -np.inf
        best_j = int(np.argmax(scores))
        print(
            f"\nSentence {i+1} is closest to Sentence {best_j+1} "
            f"(score={sim[i, best_j]:.3f})"
        )
        print(f"- {SENTENCES[i]}")
        print(f"-> {SENTENCES[best_j]}")

    print("\nDone.\n")


if __name__ == "__main__":
    main()

