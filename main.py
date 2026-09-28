from src.ingest import load_and_chunk_documents, embed_chunks
from src.store import VectorStore
from src.retrieval import secure_search


def build_index():
    print("Loading and chunking documents...")
    chunks = load_and_chunk_documents()

    print(f"Embedding {len(chunks)} chunks...")
    chunks = embed_chunks(chunks)

    store = VectorStore()
    store.add_chunks(chunks)

    print("Index built.\n")
    return store


def demo_query(store, username, query):
    print(f"--- {username} asks: \"{query}\" ---")
    results = secure_search(username, query, store)

    if not results:
        print("No accessible results found.\n")
        return

    for chunk, score in results:
        print(f"  [{score:.3f}] ({chunk['source']}) {chunk['text'][:80]}...")
    print()


if __name__ == "__main__":
    store = build_index()

    demo_query(store, "alice", "what is our deployment process?")
    demo_query(store, "alice", "what is the company's revenue?")
    demo_query(store, "bob", "what is our PTO policy?")
    demo_query(store, "carol", "what is our revenue growth?")
    demo_query(store, "dave", "what integrations do you support?")
    demo_query(store, "dave", "what is the deployment process?")
