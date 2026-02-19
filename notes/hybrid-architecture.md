# Hybrid Architecture: Graph + Vector + LLM

Modern AI systems combine **graph**, **vector search**, and **LLM** instead of choosing one. This note summarizes the pattern and how it fits this repo.

---

## Why Hybrid?

- **Graph** — Exact relationship queries (multi-hop, who works where, fraud paths).
- **Vector** — Semantic similarity (find documents or entities “like this”).
- **LLM** — Natural language in, reasoning and answer out.

Each covers different weaknesses of the others. Together they support both precise logic and semantic search.

---

## High-Level Flow

```
User question (natural language)
        ↓
   ┌────┴────┐
   ↓         ↓
Graph      Vector
query      search
(facts)    (context)
   ↓         ↓
   └────┬────┘
        ↓
   Combined context
        ↓
      LLM
        ↓
   Final answer
```

- **Graph path:** e.g. NL → Cypher (or agent tool) → run on Neo4j → structured facts.
- **Vector path:** embed question (or key phrases), retrieve similar chunks/nodes → textual context.
- **Combine:** pass facts + context to the LLM with the question; LLM generates the answer.

---

## What This Repo Covers

| Phase | Component | What you build |
|-------|-----------|----------------|
| 1–2 | Graph | Ingest, schema, Cypher, NL→Cypher |
| 7 (plan) | Hybrid | Vector store + graph + RAG-style pipeline |
| 8 (plan) | Agent | Tools: run Cypher, search graph (and optionally vector) |

So you go from **graph only** → **graph + NL** → **graph + vector + LLM** (hybrid) → **agent with graph (and vector) tools**.

---

## Design Principles

1. **Graph for structure** — Relationships, filters, and multi-hop logic stay in the graph (Cypher).
2. **Vector for semantics** — “Similar to this” and document-level search use embeddings.
3. **LLM as orchestrator** — Decides what to query (graph vs vector or both), then answers from combined context.
4. **Validate and constrain** — Don’t run arbitrary Cypher; don’t merge raw LLM extractions without schema checks.

See [plan.md](../plan.md) for the full roadmap and [rag-vs-knowledge-graph.md](rag-vs-knowledge-graph.md) for when to use graph vs RAG.
