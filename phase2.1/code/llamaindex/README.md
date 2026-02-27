# LlamaIndex — KG creation

Use LlamaIndex’s knowledge graph index and property graph to build a knowledge graph. Code is split into **graph**, **ingest**, **llm**, and **core** so you can swap LLMs and keep things modular.

**Docs:** [LlamaIndex Knowledge Graph](https://docs.llamaindex.ai/en/stable/module_guides/storing/vector_stores/), [Property Graph](https://docs.llamaindex.ai/en/stable/examples/index_structs/knowledge_graph/).

---

## Folder layout

| Folder | Purpose |
|--------|---------|
| **`core/`** | Config and shared settings (`config.py`). |
| **`graph/`** | Schema, Neo4j connection, and graph builder (`schema.py`, `connection.py`, `builder.py`). |
| **`ingest/`** | Load and parse source data from `data/` (`load_data.py`). |
| **`llm/`** | LLM interface and providers. Use different LLMs by adding or choosing a provider. |
| **`llm/providers/`** | One file per provider: `groq.py`, `openai.py`, `anthropic.py`. Add more as needed. |

All modules are stubs; fill them as you learn. Use `core/config.py` to choose which LLM provider to use (e.g. via env or config).
