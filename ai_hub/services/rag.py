import hashlib
import os
import time
from typing import List, Dict, Tuple

import joblib
import numpy as np
from django.conf import settings

try:
    import faiss  # type: ignore
    FAISS_AVAILABLE = True
except Exception:
    FAISS_AVAILABLE = False

from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize


RAG_INDEX_PATH = os.path.join(settings.AI_HUB_ARTIFACTS_DIR, "rag_index.faiss")
RAG_META_PATH = os.path.join(settings.AI_HUB_ARTIFACTS_DIR, "rag_meta.joblib")


def _read_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def _read_pdf(path: str) -> str:
    reader = PdfReader(path)
    parts = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return "\n".join(parts)


def load_docs_from_dir(directory: str) -> List[Dict]:
    docs = []
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if not os.path.isfile(path):
            continue
        if name.lower().endswith(".txt"):
            text = _read_txt(path)
        elif name.lower().endswith(".pdf"):
            text = _read_pdf(path)
        else:
            continue
        checksum = hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()
        docs.append({"name": name, "path": path, "text": text, "checksum": checksum})
    return docs


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
        if start < 0:
            start = 0
    return [c.strip() for c in chunks if c.strip()]


def build_index(docs: List[Dict], top_k: int = 3) -> Dict:
    texts = []
    meta = []
    for doc in docs:
        for chunk in chunk_text(doc["text"]):
            texts.append(chunk)
            meta.append(
                {
                    "source": doc["name"],
                    "path": doc["path"],
                    "snippet": chunk[:300],
                }
            )

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(texts)
    vectors = normalize(vectors, norm="l2")
    vectors_dense = vectors.toarray().astype("float32")

    index = None
    if settings.RAG_PROVIDER == "faiss" and FAISS_AVAILABLE:
        index = faiss.IndexFlatIP(vectors_dense.shape[1])
        index.add(vectors_dense)
        faiss.write_index(index, RAG_INDEX_PATH)

    joblib.dump(
        {
            "vectorizer": vectorizer,
            "texts": texts,
            "meta": meta,
            "vectors": vectors_dense,
            "rag_provider": settings.RAG_PROVIDER,
        },
        RAG_META_PATH,
    )
    return {"count": len(texts), "top_k": top_k}


def _load_meta():
    if not os.path.exists(RAG_META_PATH):
        return None
    return joblib.load(RAG_META_PATH)


def retrieve(query: str, top_k: int = 3) -> Tuple[List[Dict], float]:
    start = time.time()
    meta = _load_meta()
    if not meta:
        return [], 0.0

    vectorizer = meta["vectorizer"]
    vectors_dense = meta["vectors"]
    texts = meta["texts"]
    meta_rows = meta["meta"]

    q_vec = vectorizer.transform([query])
    q_vec = normalize(q_vec, norm="l2").toarray().astype("float32")

    scores = None
    indices = None
    if settings.RAG_PROVIDER == "faiss" and FAISS_AVAILABLE and os.path.exists(RAG_INDEX_PATH):
        index = faiss.read_index(RAG_INDEX_PATH)
        scores, indices = index.search(q_vec, top_k)
    else:
        sims = np.dot(vectors_dense, q_vec.T).ravel()
        indices = np.argsort(-sims)[:top_k].reshape(1, -1)
        scores = sims[indices]

    results = []
    for score, idx in zip(scores[0], indices[0]):
        results.append(
            {
                "text": texts[idx],
                "score": float(score),
                "source": meta_rows[idx]["source"],
                "snippet": meta_rows[idx]["snippet"],
            }
        )

    latency_ms = int((time.time() - start) * 1000)
    return results, latency_ms
