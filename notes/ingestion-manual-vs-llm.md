# Ingestion: Manual vs LLM-Based

When to ingest data into the graph **programmatically** (no LLM) vs **using an LLM** to extract entities and relationships.

---

## Two kinds of ingestion

| Kind | Input | How it works | When to use |
|------|--------|--------------|-------------|
| **Manual / programmatic** | Structured data (CSV, JSON, DB) | Your code parses rows/fields and runs Cypher (e.g. MERGE) to create nodes and relationships. No LLM. | When you already have clear structure (columns, keys). |
| **LLM-based** | Unstructured or semi-structured text (articles, PDFs, emails) | LLM is prompted to extract entities and relationship types from text; you validate and then run Cypher to merge into Neo4j. | When the source has no fixed schema or you want the LLM to infer structure. |

---

## Structured data → use manual ingestion

If the data is **already structured** (e.g. `movie.csv` with columns: movie_id, movie_name, director, genre, cast):

- You already have the “schema” in the columns.
- A small script can map those fields to Cypher (MERGE nodes/relationships) in a **deterministic** way.
- That’s **fast, cheap, and reliable**. No need for an LLM.

Using an LLM to “extract” from structured data is possible but **usually not worth it**: you add cost, latency, and risk (hallucination, format drift) without real benefit.

**In this repo:** Phase 1 and phase2.1 movie data use **manual ingestion** (e.g. `ingest/load_data.py` + `graph/builder.py` or equivalent).

---

## Unstructured text → LLM-based ingestion makes sense

LLM-based ingestion is for when the **source has no clear structure**:

- Unstructured: articles, reports, PDFs, emails, chat logs.
- Semi-structured: mixed formats, or you want to infer **new** entity/relationship types that aren’t in the original data.

Then the LLM’s job is to **create** structure: “From this text, list entities and relationships (with types).” You validate that output (e.g. against your ontology/schema) and merge into the graph with Cypher.

**In this repo:** This is the focus of **Phase 6** (LLM for graph — extraction pipeline) in [plan.md](../plan.md).

---

## Summary

- **Structured data (CSV, JSON, etc.)** → **Manual ingestion**: code + Cypher. No LLM for ingestion.
- **Unstructured (or semi-structured) text** → **LLM-based ingestion**: LLM extracts entities/relations → validate → merge into graph.
- You *can* use an LLM on structured data for ingestion, but it’s redundant; the normal and recommended approach for structured data is programmatic ingestion.

---

*See also: [LangChain framework and usage](langchain-framework-and-usage.md), [Glossary](glossary.md), [Plan Phase 6](../plan.md).*
