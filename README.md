# Multi-Tenant RAG with Permission-Aware Retrieval

A RAG (Retrieval-Augmented Generation) system that enforces role-based access control at the retrieval layer — before any content reaches a language model or the end user. Includes semantic search via local embeddings, permission filtering, and full audit logging.

## The problem this solves

Most RAG tutorials assume every document is visible to every user. In real organizations, this is never true: HR documents shouldn't be visible to engineers, financial reports shouldn't be visible to customers, and so on. A naive RAG system built without access control will happily retrieve and surface exactly the wrong document to the wrong person, since it only optimizes for semantic relevance — not permissions.

This project demonstrates the fix: every retrieval result is checked against the requesting user's role *before* it's returned, and every query is logged for auditability.

## Architecture