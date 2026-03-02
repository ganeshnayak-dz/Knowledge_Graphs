# LangChain — KG creation

Use LangChain’s graph and Neo4j integrations to build a knowledge graph. Code is split into **db**, **graph**, **ingest**, **llm**, and **core** so you can swap LLMs and keep connection logic in one place.

**Docs:** [LangChain Graph](https://python.langchain.com/docs/use_cases/graph/), [Neo4j integration](https://python.langchain.com/docs/integrations/graphs/neo4j/).

---

## Quick start

1. **Install:** `pip install -r requirements.txt`
2. **Configure:** Copy or edit `.env` with Neo4j and LLM settings (see below).
3. **Ingest:** `python main.py` — loads data into Neo4j using `graph/schema.py` and `ingest/load_data.py`.
4. **Ask:** `python ask.py` — interactive NL→Cypher; type a question, press Enter. Type `exit` or `quit` to stop.

**Neo4j:** For a **local** instance (e.g. Neo4j Desktop), set `NEO4J_URI=bolt://127.0.0.1:7687` (use `bolt://`, not `neo4j://`, to avoid “Unable to retrieve routing information”).  
**APOC:** The NL→Cypher chain uses Neo4j’s schema; if you see “Could not use APOC procedures”, install and enable the APOC plugin in Neo4j, or use a manual schema (e.g. `refresh_schema=False` and set `graph.schema` in `db/connection.py`).

---

## Folder layout

| Folder | Purpose |
|--------|---------|
| **`core/`** | Config and shared settings (`config.py`). |
| **`db/`** | **Single place for Neo4j:** `connection.py` has `get_neo4j_connection()` (ingest) and `get_graph()` → `Neo4jGraph` for the NL→Cypher chain. |
| **`graph/`** | Schema and Cypher templates (`schema.py`) for constraints and MERGEs; optional builder. |
| **`ingest/`** | Load and parse source data from `data/` (`load_data.py`). |
| **`llm/`** | LLM interface and providers; `get_llm_for_chain()` returns the chat model for chains. |
| **`llm/providers/`** | One file per provider: `groq.py`, etc. Add more as needed. |
| **`nl2cypher/`** | NL→Cypher via **`langchain_neo4j`** `GraphCypherQAChain` (`chain.py`). Uses `get_graph()` and `get_llm_for_chain()`. |
| **`models/`** | Pydantic models for ingest (e.g. `movie.py`). |

---

## Config (`.env`)

- **Neo4j:** `NEO4J_URI` (use `bolt://...` for local), `NEO4J_USER`, `NEO4J_PASSWORD`, `NEO4J_DB`.
- **LLM:** `LLM_PROVIDER=groq`, `GROQ_API_KEY`, `GROQ_MODEL` (or other provider vars).

Run scripts from this directory so imports like `db.connection` and `nl2cypher.chain` resolve.

---

## Modularity and readability

- **Single responsibility:** `core/` = config, `db/` = Neo4j (ingest driver + LangChain graph), `graph/` = schema and Cypher, `ingest/` = load CSV → Neo4j, `llm/` = one entry point (`get_llm`, `get_llm_for_chain`) and one implementation per provider in `llm/providers/`, `nl2cypher/` = build and run the QA chain only.
- **One source of truth:** LLM for chains comes from `llm.get_llm_for_chain()` (implemented in `llm/providers/groq.py`); root `__init__.py` only re-exports. Neo4j credentials live in `core.config.settings` and are used only in `db/connection.py`.
- **Clear boundaries:** Ingest uses `get_neo4j_connection()` and `graph.schema`; NL→Cypher uses `get_graph()` and `get_llm_for_chain()`. No cross-calls between ingest and nl2cypher.
- **Docstrings** on modules and public functions; section comments in `graph/schema.py` (constraints vs MERGE templates). DB connection is always closed in ingest (try/finally).
