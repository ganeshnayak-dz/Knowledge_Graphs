# Phase 2 — Natural Language → Cypher (NL2Cypher)

Phase 2 adds an **LLM** (e.g. Groq) to translate natural language questions into **Cypher** and run them on the Neo4j graph. You ask in plain English; the system generates Cypher, validates it, executes it, and returns results.

---

## Overview

| What | Description |
|------|-------------|
| **Goal** | Ask questions about the graph in natural language; get answers via generated Cypher. |
| **Dataset** | Employee data (`data/employee.csv`): name, age, gender, department, position, salary, etc. |
| **Graph** | Employees, Departments, Positions; relationships WORKS_IN and HAS_ROLE. |
| **LLM** | Groq by default; swappable (e.g. Gemini) via `llm/providers/` and `.env`. |
| **Schema** | Generated from Neo4j and saved to a file so we don’t query the DB on every question. |

---

## Prerequisites

- **Python 3.10+**
- **Neo4j** (Desktop or Docker) running and reachable (e.g. `neo4j://127.0.0.1:7687`)
- **Groq API key** (or another LLM; see [Switching LLM](#switching-llm))

---

## Graph Schema (Phase 2)

- **Nodes**
  - **Employee:** `name`, `age`, `gender`, `salary`, `department`, `position`, `joining_date`, `productivity`, etc.
  - **Department:** `department`
  - **Position:** `position`
- **Relationships**
  - `(Employee)-[:WORKS_IN]->(Department)`
  - `(Employee)-[:HAS_ROLE]->(Position)`

Constraints ensure uniqueness on `Employee.name`, `Department.department`, and `Position.position`.

---

## Setup

### 1. Create a virtual environment (recommended)

```bash
cd phase2/code
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Copy the example env and fill in your values:

```bash
cp env.example .env
```

Edit `.env`:

- **Neo4j:** `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`, `NEO4J_DB`
- **Groq:** `GROQ_API_KEY`, `GROQ_MODEL` (e.g. `llama-3.1-70b-versatile`)

Optional: `LLM_PROVIDER`, `SCHEMA_FILE` (see [Configuration](#configuration)).

---

## Folder Structure

```
phase2/
├── README.md                 # This file
├── data/
│   └── employee.csv         # Input dataset
└── code/
    ├── main.py               # Ingest: load CSV into Neo4j
    ├── ask.py                # Interactive Q&A (natural language → Cypher → results)
    ├── requirements.txt
    ├── .env                  # Your config (not committed)
    ├── env.example           # Template for .env
    ├── core/
    │   └── config.py         # Settings (Neo4j, LLM, schema path)
    ├── db/
    │   └── connection.py     # Neo4j connection
    ├── graph/
    │   └── schema.py        # Cypher for ingestion (constraints, MERGEs)
    ├── ingest/
    │   └── load_data.py      # CSV → validation → Neo4j
    ├── models/
    │   └── employee.py       # Pydantic model for validation
    ├── llm/                  # LLM abstraction (swap provider here)
    │   ├── base.py           # Protocol: generate(system, user) -> str
    │   ├── __init__.py       # get_llm()
    │   └── providers/
    │       ├── groq.py       # Groq implementation
    │       └── ...
    ├── nl2cypher/            # NL → Cypher pipeline
    │   ├── prompts.py        # System prompt (generic, no hardcoded schema)
    │   ├── cypher_utils.py   # Extract Cypher from LLM output, read-only check
    │   ├── pipeline.py      # ask_graph(question) -> {query, results}
    │   └── prompt_schema/   # Generated schema (do not edit by hand)
    │       └── graph_schema.txt
    └── scripts/
        └── generate_schema.py  # Introspect Neo4j, write schema to prompt_schema/
```

---

## How to Run

All commands below are run from **`phase2/code`**.

### 1. Ingest data (first time or after CSV change)

Load the employee CSV into Neo4j:

```bash
python main.py
```

### 2. Generate the schema (first time or after graph structure changes)

Introspect Neo4j and save the schema so the LLM knows labels, properties, and relationships:

```bash
python scripts/generate_schema.py
```

This writes `nl2cypher/prompt_schema/graph_schema.txt`. The ask pipeline reads this file on each question.

### 3. Ask questions

Start the interactive Q&A loop:

```bash
python ask.py
```

Then type natural language questions, e.g.:

- “Get all positions”
- “Which employees work in HR?”
- “Count of Female employees who work in HR department”

Type `exit` or `quit` to stop. Results and the generated Cypher are printed (set `VERBOSE = False` in `ask.py` to hide raw/generated Cypher).

---

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `NEO4J_URI` | Neo4j Bolt URI | `neo4j://127.0.0.1:7687` |
| `NEO4J_USER` | Neo4j user | `neo4j` |
| `NEO4J_PASSWORD` | Neo4j password | — |
| `NEO4J_DB` | Database name | `emp` |
| `LLM_PROVIDER` | `groq` or `gemini` (etc.) | `groq` |
| `GROQ_API_KEY` | Groq API key | — |
| `GROQ_MODEL` | Groq model name | — |
| `SCHEMA_FILE` | Path to schema file (relative to `code/` or absolute) | `nl2cypher/prompt_schema/graph_schema.txt` |

---

## Switching LLM

The LLM is behind a small abstraction in `llm/`. To use another provider (e.g. Gemini):

1. Add a new provider in `llm/providers/` (e.g. `gemini.py`) that implements `generate(system, user, max_tokens) -> str`.
2. Add the provider’s config (e.g. `GEMINI_API_KEY`, `GEMINI_MODEL`) to `core/config.py` and `.env`.
3. In `llm/__init__.py`, extend `get_llm()` to return the new provider when `LLM_PROVIDER=gemini` (or your name).
4. Set `LLM_PROVIDER=gemini` in `.env`.

Prompts and the rest of the pipeline stay unchanged.

---

## Security

- Only **read-only** Cypher is allowed (MATCH, RETURN, WHERE, WITH, ORDER BY, LIMIT). Queries containing CREATE, MERGE, DELETE, SET, REMOVE, or DROP are rejected.
- Do not commit `.env`; use `env.example` as a template.

---

## Troubleshooting

| Issue | What to do |
|-------|------------|
| “Schema file not found” | Run `python scripts/generate_schema.py` from `phase2/code`. |
| “Connection refused” to Neo4j | Start Neo4j and check `NEO4J_URI`, port 7687. |
| “No Cypher found in LLM response” | The model may have returned prose; try rephrasing the question or check the prompt. |
| Wrong or empty results | Check the generated Cypher in the output; ensure relationship direction and property names match the schema. |

For more detail on the schema and scripts, see **`code/README.md`**.
