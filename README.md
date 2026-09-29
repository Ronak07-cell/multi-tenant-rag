# Multi-Tenant RAG with Permission-Aware Retrieval

A RAG (Retrieval-Augmented Generation) system that enforces role-based access control at the retrieval layer — before any content reaches a language model or the end user. Includes semantic search via local embeddings, permission filtering, and full audit logging.

## The problem this solves

Most RAG tutorials assume every document is visible to every user. In real organizations, this is never true: HR documents shouldn't be visible to engineers, financial reports shouldn't be visible to customers, and so on. A naive RAG system built without access control will happily retrieve and surface exactly the wrong document to the wrong person, since it only optimizes for semantic relevance — not permissions.

This project demonstrates the fix: every retrieval result is checked against the requesting user's role *before* it's returned, and every query is logged for auditability.

## Architecture

- **`src/auth.py`** — user/role definitions and per-document access rules
- **`src/ingest.py`** — chunks documents and creates embeddings using a free, local model (`all-MiniLM-L6-v2`, via `sentence-transformers`) — no API key or cost required
- **`src/store.py`** — a simple in-memory vector store using cosine similarity for semantic search
- **`src/retrieval.py`** — the core security logic: searches broadly, then discards any result the user's role isn't permitted to see, before returning anything
- **`src/audit.py`** — logs every query with timestamp, user, role, and exactly which sources were (and weren't) returned, to `audit_log.jsonl`

## Demonstrated behavior

Running `main.py` proves the access control works even in adversarial-looking cases:
- An engineer asking about company revenue gets **zero results** — despite the finance report being the most semantically relevant document — because engineers aren't authorized to see it
- A customer asking an innocent-sounding question about "deployment process" gets **zero results** from internal engineering docs, for the same reason
- Every one of these decisions is recorded in the audit log, creating a compliance-style trail of who accessed what

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## Tech stack

- Python 3
- `sentence-transformers` (local embeddings, `all-MiniLM-L6-v2`)
- `numpy` (cosine similarity)
- No external API calls required for the retrieval/security pipeline

## Next step (not yet implemented): answer generation

This project currently returns the permission-filtered *chunks* themselves — the "Retrieval" half of RAG. The final step — feeding those chunks to an LLM to generate a natural-language answer — is a well-understood, separate layer that can be added with either:
- A local model via Ollama (free, runs on-device, no API key)
- A hosted API (Anthropic, OpenAI, etc.)

The retrieval and security architecture is intentionally decoupled from generation, so either option plugs in without changing anything upstream.

## What I learned

- Building a permission model as a genuinely separate, auditable layer — not scattered through business logic
- Embedding-based semantic search: cosine similarity, why over-fetching before filtering is necessary to guarantee a full result set after permission checks
- Why audit logging matters for compliance in any system handling access-controlled data
- The tradeoff between local-only (free, private, no rate limits) and API-based (higher quality, but cost and data-sharing considerations) approaches to the generation step