# LangChain: Framework vs Custom Pipeline

Quick reference for what “using the LangChain framework” means in this repo, and where things go in **phase2.1/code/langchain**.

---

## What “the framework” means

- **Using the framework** = Using LangChain’s **built-in chains and integrations** (e.g. `GraphCypherQAChain`), so you don’t write the full NL→Cypher→run→answer pipeline yourself.
- **Not using the framework** = You wire each step yourself: your prompt + `llm.generate()` + regex to get Cypher + `graph.query()` + format the answer. You might still use LangChain for the LLM client (`ChatGroq`) and the graph client (`Neo4jGraph`), but the *orchestration* is custom.

So: **framework = the chain** (e.g. `GraphCypherQAChain.from_llm(...)` and `chain.invoke(...)`), not just the low-level libraries.

---

## Two ways to do “question → graph → answer”

| Approach | What you do |
|----------|-------------|
| **Custom pipeline** | You write: prompt → call LLM → extract Cypher → validate → run on Neo4j → (optional) LLM to format answer. |
| **Framework (chain)** | You use e.g. `GraphCypherQAChain.from_llm(llm, graph, ...)` and `chain.invoke({"query": question})`. LangChain does prompt, Cypher generation, execution, and optional answer step. |

For phase2.1, using **`GraphCypherQAChain`** from `langchain_community.chains.graph_qa.cypher` is the intended “framework” approach.

---

## What the chain needs

Only two inputs:

1. **`llm`** — A LangChain chat model (e.g. `ChatGroq` from `langchain_groq`), created with your API key and model.
2. **`graph`** — A LangChain Neo4j graph (`Neo4jGraph` from `langchain_neo4j`), created with Neo4j URL, user, password, database.

Dependencies: `langchain`, `langchain_community`, `langchain_neoj`, `langchain_groq` (or other LLM package).

---

## Where things go in phase2.1

| Place | Purpose |
|-------|---------|
| **`core/config.py`** | Env/settings only. No LangChain imports. |
| **`db/connection.py`** | **Single place for Neo4j:** `get_neo4j_connection()` for ingest; `get_graph()` → `Neo4jGraph` for chains. Same config for both. |
| **`graph/schema.py`** | Schema and Cypher templates. No connection logic. |
| **`llm/providers/groq.py`** | LangChain `ChatGroq`; implements `LLMProvider` for custom use. |
| **`llm/__init__.py`** | Expose `get_llm()` and `get_llm_for_chain()` (raw LangChain model for the chain). |
| **`nl2cypher/chain.py`** | Builds `GraphCypherQAChain.from_llm(get_llm_for_chain(), get_graph(), ...)`; `get_graph()` from `db.connection`. Exposes `ask_graph(question)`. |
| **`ask.py`** | Thin CLI: parse question, call `ask_graph(question)`, print result. |

Ingestion (CSV → graph) stays **manual**: `ingest/load_data.py` parses data, uses `get_neo4j_connection()` and `graph.schema` to run Cypher MERGEs. No chain involved.

---

## Safety note

`GraphCypherQAChain` can run whatever Cypher the LLM generates. The flag **`allow_dangerous_requests=True`** is required to allow execution; use it only when you accept that risk (e.g. read-only validation elsewhere, or trusted environments).

---

*See also: [Ingestion: manual vs LLM](ingestion-manual-vs-llm.md), [Glossary](glossary.md).*
