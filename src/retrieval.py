from src.ingest import model
from src.auth import get_user, can_access
from src.audit import log_retrieval


def secure_search(username, query, vector_store, top_k=5):
    user = get_user(username)

    if user is None:
        raise ValueError(f"Unknown user: {username}")

    role = user["role"]

    query_embedding = model.encode(query)

    raw_results = vector_store.search(query_embedding, top_k=top_k * 3)

    filtered_results = []
    for chunk, score in raw_results:
        if can_access(role, chunk["source"]):
            filtered_results.append((chunk, score))
        if len(filtered_results) >= top_k:
            break

    log_retrieval(username, role, query, filtered_results)

    return filtered_results
  
