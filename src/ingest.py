import os
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def chunk_text(text, chunk_size=200):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks


def load_and_chunk_documents(directory="data/documents"):
    all_chunks = []

    for filename in os.listdir(directory):
        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(directory, filename)
        with open(filepath, "r") as f:
            text = f.read()

        chunks = chunk_text(text)

        for chunk in chunks:
            all_chunks.append({
                "text": chunk,
                "source": filename
            })

    return all_chunks


def embed_chunks(chunks):
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts)

    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding

    return chunks
