import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from typing import List, Tuple, Dict, Any

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI


DEFAULT_EMBED_MODEL = "text-embedding-3-small"

STOPWORDS = {
    "the", "a", "an", "and", "or", "to", "of", "in", "on", "for", "with", "is",
    "are", "was", "were", "be", "been", "being", "that", "this", "it", "as",
    "after", "before", "by", "from", "at", "we", "you", "your", "our", "they",
    "them", "their", "into", "until", "then"
}


# ---------------- Utilities ----------------

def load_lines(path: Path) -> List[str]:
    return [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


# ---------------- Keyword search ----------------

def tokenize(text: str) -> List[str]:
    words = re.findall(r"[a-z0-9']+", text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 1]


def keyword_score(query: str, doc: str) -> float:
    """
    Simple, fair keyword scoring:
    overlap(query_terms, doc_terms) / len(query_terms)
    """
    q_terms = set(tokenize(query))
    if not q_terms:
        return 0.0
    d_terms = set(tokenize(doc))
    return len(q_terms.intersection(d_terms)) / len(q_terms)


def keyword_search(query: str, docs: List[str], top_k: int) -> List[Tuple[float, int]]:
    scored = [(keyword_score(query, d), i) for i, d in enumerate(docs)]
    scored.sort(reverse=True, key=lambda x: x[0])
    # only keep >0 matches
    return [(s, i) for s, i in scored if s > 0][:top_k]


# ---------------- Similarity search (embeddings) ----------------

def get_embeddings(client: OpenAI, texts: List[str], model: str) -> np.ndarray:
    resp = client.embeddings.create(model=model, input=texts)
    vectors = [item.embedding for item in resp.data]
    return np.array(vectors, dtype=np.float32)


def build_or_load_embedding_cache(
    client: OpenAI,
    knowledge_path: Path,
    cache_path: Path,
    embed_model: str,
) -> Dict[str, Any]:
    """
    Builds embeddings for each line in knowledge.txt and caches to disk.
    Reuses cache if file hash + embedding model match.
    """
    file_hash = sha256_file(knowledge_path)

    if cache_path.exists():
        cached = json.loads(cache_path.read_text(encoding="utf-8"))
        if cached.get("file_sha256") == file_hash and cached.get("embed_model") == embed_model:
            return cached

    lines = load_lines(knowledge_path)
    vectors = get_embeddings(client, lines, model=embed_model)

    data = {
        "embed_model": embed_model,
        "file_sha256": file_hash,
        "lines": lines,
        "vectors": vectors.tolist(),
    }
    cache_path.write_text(json.dumps(data), encoding="utf-8")
    return data


def similarity_search(query: str, lines: List[str], vectors: np.ndarray, client: OpenAI, embed_model: str, top_k: int):
    q_vec = get_embeddings(client, [query], model=embed_model)[0]
    scored = [(cosine_similarity(q_vec, vectors[i]), i) for i in range(len(lines))]
    scored.sort(reverse=True, key=lambda x: x[0])
    return scored[:top_k]


# ---------------- Main ----------------

def main():
    parser = argparse.ArgumentParser(description="Keyword vs similarity search over knowledge.txt (ransomware).")
    parser.add_argument("--text", required=True, help="Query text, e.g. \"Best way to recover from malware\"")
    parser.add_argument("--type", choices=["keyword", "similarity", "both"], default="both",
                        help="Search type (default: both)")
    parser.add_argument("--top", type=int, default=3, help="Top results to return (default: 3)")
    parser.add_argument("--file", default="knowledge.txt", help="Knowledge file (default: knowledge.txt)")
    parser.add_argument("--model", default=DEFAULT_EMBED_MODEL, help=f"Embedding model (default: {DEFAULT_EMBED_MODEL})")
    parser.add_argument("--rebuild", action="store_true", help="Force rebuild embedding cache")
    args = parser.parse_args()

    base_dir = Path(__file__).parent
    knowledge_path = (base_dir / args.file).resolve()
    if not knowledge_path.exists():
        raise FileNotFoundError(f"Knowledge file not found: {knowledge_path}")

    lines = load_lines(knowledge_path)

    print("\n=== Query ===")
    print(args.text)

    # Keyword search doesn't need API
    if args.type in ("keyword", "both"):
        kw = keyword_search(args.text, lines, top_k=args.top)
        print("\n=== Keyword Search Results ===")
        if not kw:
            print("(no matches found)")
        else:
            for rank, (score, idx) in enumerate(kw, start=1):
                print(f"\n#{rank}  score={score:.3f}  line={idx+1}")
                print(lines[idx])

    # Similarity search needs API key + cache
    if args.type in ("similarity", "both"):
        env_path = base_dir / ".env"
        load_dotenv(dotenv_path=env_path, override=True)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(f"OPENAI_API_KEY not found. Create {env_path} from .env.example.")

        client = OpenAI(api_key=api_key)

        cache_path = base_dir / f"{knowledge_path.stem}.{args.model}.cache.json"
        if args.rebuild and cache_path.exists():
            cache_path.unlink()

        idx_data = build_or_load_embedding_cache(client, knowledge_path, cache_path, args.model)
        vectors = np.array(idx_data["vectors"], dtype=np.float32)

        sims = similarity_search(args.text, idx_data["lines"], vectors, client, args.model, top_k=args.top)

        print("\n=== Similarity Search Results ===")
        for rank, (score, idx) in enumerate(sims, start=1):
            print(f"\n#{rank}  score={score:.4f}  line={idx+1}")
            print(idx_data["lines"][idx])

        print(f"\n(Cache: {cache_path.name})")

    print("\nDone.\n")


if __name__ == "__main__":
    main()
