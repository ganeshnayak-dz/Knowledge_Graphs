# Code — Phase 2.1

One folder per framework. **Inside each framework** the layout is the same so code stays organized and you can swap LLMs easily:

| Folder | Purpose |
|--------|---------|
| **`core/`** | Config (Neo4j, API keys; which LLM provider to use). |
| **`graph/`** | Schema, connection, and graph builder. |
| **`ingest/`** | Load and parse source data from `../data/` or Phase 1/2 data. |
| **`llm/`** | LLM interface (`base.py`) and **`llm/providers/`** — one file per provider (Groq, OpenAI, Anthropic). Add more as needed. |

| Framework folder | |
|------------------|---|
| `langchain/` | LangChain |
| `llamaindex/` | LlamaIndex |
| `haystack/` | Haystack |

All modules are stubs. Fill as you learn; add new LLM providers under `llm/providers/` and select them via config.
