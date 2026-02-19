# Phase 2 Code

## Schema (for NL → Cypher)

The pipeline uses a **saved schema file** so we don't query Neo4j on every question.

- **Where:** `nl2cypher/prompt_schema/graph_schema.txt` (generated; do not edit by hand).
- **When to update:** After the graph structure changes (new labels, relationships, or ingestion).

### Generate or update the schema

From **phase2/code** (this directory):

```bash
python scripts/generate_schema.py
```

Or:

```bash
python -m scripts.generate_schema
```

This introspects Neo4j (labels and relationship structure), writes the schema to `nl2cypher/prompt_schema/graph_schema.txt`, and prints it. The next time you run an "ask" flow, the pipeline will use this file.

### Override schema file location

In `.env`:

```env
SCHEMA_FILE=path/to/other_schema.txt
```

Paths are relative to **phase2/code** unless absolute.

## Folder layout

```
phase2/code/
├── main.py              # Ingest entry (e.g. python main.py)
├── scripts/
│   └── generate_schema.py   # Run to refresh schema
├── core/                 # Config (Neo4j, LLM, schema path)
├── db/                   # Neo4j connection
├── graph/                # Cypher for ingestion (graph/schema.py)
├── ingest/               # CSV → Neo4j
├── llm/                  # LLM abstraction (Groq, etc.)
├── nl2cypher/            # Prompts, pipeline (ask_graph)
│   └── prompt_schema/   # Generated schema (run scripts/generate_schema.py)
│       └── graph_schema.txt
└── models/               # Pydantic models
```
