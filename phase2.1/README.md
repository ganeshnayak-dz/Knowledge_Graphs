# Phase 2.1 — KG Creation with Frameworks (LangChain, LlamaIndex, Haystack)

**Purpose:** Explore different frameworks for building and working with Knowledge Graphs. Same top-level layout as Phase 2: **code** and **data** in separate folders. Under `code/`, one folder per framework; each uses the same modular pattern. Fill in the code as you learn.

**Relation to plan:** Complements Phase 2 (NL→Cypher) and Phase 3 (graph engineering). Use this phase to compare how each framework handles graph construction and integration.

---

## Folder layout (like Phase 2)

| Folder   | Contents |
|----------|----------|
| **`code/`** | One subfolder per framework: `langchain/`, `llamaindex/`, `haystack/`. Inside each: **core/** (config), **graph/** (schema, connection, builder), **ingest/** (load_data), **llm/** (base + providers for Groq, OpenAI, Anthropic). Same layout so you can swap LLMs and keep things modular. |
| **`data/`** | Shared or framework-specific input data (CSV, JSON, etc.). Keeps data separate from code. |

So: **code** and **data** are separate; frameworks live under **code**.

---

## Frameworks (3)

| Folder        | Framework   | Use for |
|---------------|-------------|--------|
| `code/langchain/`  | LangChain   | KG indexing, graph builders, Neo4j integration. |
| `code/llamaindex/`  | LlamaIndex  | Knowledge graph index, property graph, Neo4j. |
| `code/haystack/`   | Haystack    | Document stores, pipelines, graph-friendly RAG/KG. |

Add more by copying one framework folder and renaming it (e.g. `code/custom/`).

---

## Modular folder pattern (per framework)

Each framework folder under `code/` uses the same layout:

- **`core/`** — `config.py` (Neo4j, API keys, paths; choose LLM provider here).
- **`graph/`** — `schema.py`, `connection.py`, `builder.py` (schema, Neo4j connection, KG build).
- **`ingest/`** — `load_data.py` (load/parse data from `data/` or elsewhere).
- **`llm/`** — `base.py` (interface) and **`llm/providers/`** with one file per LLM: `groq.py`, `openai.py`, `anthropic.py`. Add more providers as needed.

All modules are stubs (short docstring only). Fill as you learn; swap LLMs by implementing a new provider and selecting it in config.

---

## How to use

1. Put datasets in **`data/`** (or reference Phase 1/2 data).
2. Pick a framework under **`code/`** (e.g. `code/langchain/`).
3. Install deps from that folder’s `requirements.txt` when you add them.
4. Fill modules in order: core/config → graph/ (connection, schema, builder) → ingest/load_data → llm (base + the provider you use).
5. Repeat for another framework and compare.

---

## Prerequisites

- Phase 1 or Phase 2 graph running in Neo4j (or a blank DB).
- Python 3.10+.
- Framework-specific packages (add to each folder’s `requirements.txt` when you add code).
