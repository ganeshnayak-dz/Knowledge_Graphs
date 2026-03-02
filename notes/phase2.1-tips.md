# Phase 2.1 — Tips & What I Learnt

Short, practical tips from building the LangChain KG pipeline (phase2.1). Use these when you revisit the code or extend it.

---

## Connection: one module, two entry points

- **Keep all Neo4j connection logic in one place** (e.g. `db/connection.py`). Credentials and “how we connect” live there only.
- **Expose two entry points from that module:**
  - **`get_neo4j_connection()`** → raw driver (or `Neo4jConnection`) for **ingest** and direct Cypher. Caller creates and closes it per use.
  - **`get_graph()`** → LangChain `Neo4jGraph` for **chains** (e.g. `GraphCypherQAChain`). Can be cached and reused.
- **Why:** No duplicated credentials or connection logic; one place to add timeouts, retries, or another DB later.
- **Folder structure:** `db/` = database/connection; `graph/` = schema and Cypher templates (no connection file there).

---

## When to use which connection

| Use case | Use | Reason |
|----------|-----|--------|
| Ingest (CSV → MERGE) | `get_neo4j_connection()` or `Neo4jConnection` | You run fixed Cypher; no LangChain needed. |
| NL→Cypher (ask in natural language) | `get_graph()` → `Neo4jGraph` | LangChain chains require the graph object they provide. |

---

## Framework vs custom pipeline

- **Using the framework** = using LangChain’s **chains** (e.g. `GraphCypherQAChain.from_llm(...)` and `chain.invoke(...)`). The chain does prompt → Cypher → run → answer.
- **Custom pipeline** = you write each step (prompt, LLM call, Cypher extraction, validation, execution). You might still use `ChatGroq` and `Neo4jGraph` as building blocks.
- For phase2.1, **prefer the chain** for NL→Cypher; keep ingest as plain code + Cypher (no LLM for ingestion).

---

## Ingestion: manual vs LLM

- **Structured data (CSV, JSON)** → **Manual ingestion**: parse in code, run Cypher (MERGE). Fast, deterministic, no LLM.
- **Unstructured text** → **LLM-based ingestion**: LLM extracts entities/relations; you validate and merge. See [ingestion-manual-vs-llm.md](ingestion-manual-vs-llm.md) and plan Phase 6.

---

## Modular layout (phase2.1)

- **`core/`** — Config only (env, settings). No connection, no LLM.
- **`db/`** — Connection only. Both raw and LangChain graph from same config.
- **`graph/`** — Schema and Cypher strings. No connection; ingest and chain use `db` for that.
- **`ingest/`** — Load CSV, validate with models, call `db` + `graph.schema` to write. No LangChain.
- **`llm/`** — Provider interface and implementations. Chain gets the LangChain model via `get_llm_for_chain()`.
- **`nl2cypher/`** — Build and run the NL→Cypher chain; import `get_graph()` from `db.connection`, LLM from `llm`.
- **`models/`** — Pydantic models for ingest (e.g. movie CSV).

---

## Running

- **From** `phase2.1/code/langchain`: `python main.py` (ingest), `python ask.py "<question>"` (NL→Cypher).
- Ensure `.env` has `NEO4J_*`, `GROQ_API_KEY`, `GROQ_MODEL` (or the LLM provider you use).

---

*See also: [LangChain framework and usage](langchain-framework-and-usage.md), [Ingestion: manual vs LLM](ingestion-manual-vs-llm.md), [Glossary](glossary.md).*
