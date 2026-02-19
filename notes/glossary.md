# Glossary — Terms Used in This Repo

Short definitions for concepts in the [plan](../plan.md) and codebase. Useful when reading notes or docs.

---

## Graph & database

- **Knowledge Graph (KG)** — A graph of entities (nodes) and relationships (edges) with a schema and optional constraints. Used for structured reasoning and multi-hop queries.
- **Neo4j** — Graph database used in this project. Data is stored as nodes and relationships; queried with Cypher.
- **Cypher** — Query language for Neo4j. Example: `MATCH (a:Person)-[:ACTED_IN]->(m:Movie) RETURN m`.
- **Schema (graph)** — Which node labels and relationship types exist; what properties they have. In this repo, see `graph/schema.py` and `nl2cypher/prompt_schema/graph_schema.txt`.
- **Constraint** — Rule in the database (e.g. uniqueness on a property). Used to keep data consistent.
- **Index** — Speeds up lookups on a property or pattern. Often used with constraints.

---

## LLM & retrieval

- **RAG (Retrieval-Augmented Generation)** — Pattern: retrieve relevant text (e.g. via vector search), then pass it to an LLM to generate an answer. Works on unstructured text.
- **Vector search / embedding** — Represent text as a vector; find “similar” text by distance (e.g. cosine). Used in RAG and semantic search.
- **NL→Cypher** — Natural language → Cypher. User asks in plain English; an LLM (or chain) generates a Cypher query that is validated and run on the graph.
- **Hybrid (graph + vector)** — Combine graph queries (structured facts) and vector retrieval (semantic context), then feed both to an LLM for the final answer.

---

## Agents & tools

- **Agent** — An LLM that can decide which **tools** to call (e.g. run Cypher, search graph) and use their results to answer.
- **Tool** — A callable function the agent can use (e.g. `run_cypher`, `search_graph`). In this repo, Phase 8 adds graph (and optionally vector) tools.

---

## KG quality & design

- **Ontology** — Definition of entity types and allowed relationships (controlled vocabulary). Used to govern what goes into the KG.
- **Entity resolution** — Deciding when two mentions refer to the same real-world entity (deduplication, merging). Important for KG quality.
- **Schema governance** — Keeping the graph schema consistent; not letting arbitrary relationship types or properties be created (e.g. by an LLM) without validation.

---

## Neo4j / GDS

- **EXPLAIN** — Shows the query plan Neo4j would use (without running the query). Used for optimization.
- **PROFILE** — Runs the query and shows actual execution stats. Used to find bottlenecks.
- **GDS (Graph Data Science)** — Neo4j library for algorithms (PageRank, shortest path, community detection, similarity, etc.).
