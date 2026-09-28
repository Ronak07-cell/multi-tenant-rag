import json
from datetime import datetime

AUDIT_LOG_FILE = "audit_log.jsonl"


def log_retrieval(username, role, query, retrieved_chunks):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "username": username,
        "role": role,
        "query": query,
        "retrieved_sources": [chunk["source"] for chunk, score in retrieved_chunks],
        "num_results": len(retrieved_chunks)
    }

    with open(AUDIT_LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

    return entry
