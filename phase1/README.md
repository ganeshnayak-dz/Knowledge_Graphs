# Phase 1 — Pure Graph Foundation (No LLM)

Phase 1 focuses on **graph modeling**, **Cypher**, and **ingesting data into Neo4j**. You write Cypher by hand; there is no natural language or LLM. The goal is to build a solid graph and query layer before adding NL→Cypher in Phase 2.

---

## Overview

| What | Description |
|------|-------------|
| **Goal** | Model data as a graph, ingest into Neo4j, write and run Cypher queries by hand. |
| **Dataset** | Movie data (`data/movie.csv`): `movie_id`, `movie_name`, `year`, `overview`, `director`, `genre` (comma-separated), `cast` (comma-separated). |
| **Graph** | Movies, Genres, Persons (directors and actors); relationships HAS_GENRE, DIRECTED, ACTED_IN. |
| **LLM** | None. Queries are written in code (e.g. in `query/run.py`). |

---

## Prerequisites

- **Python 3.10+**
- **Neo4j** (Desktop or Docker) running and reachable (e.g. `neo4j://127.0.0.1:7687`)
- **pandas** (used by the ingest script; add to requirements if not already present)

---

## Graph Schema (Phase 1)

- **Nodes**
  - **Movie:** `movie_id`, `name`, `year`, `overview`
  - **Genre:** `name`
  - **Person:** `name` (used for both directors and actors)
- **Relationships**
  - `(Movie)-[:HAS_GENRE]->(Genre)` — one movie can have multiple genres
  - `(Person)-[:DIRECTED]->(Movie)` — director
  - `(Person)-[:ACTED_IN]->(Movie)` — cast (one person can act in many movies)

Constraints ensure uniqueness on `Movie.movie_id`, `Person.name`, and `Genre.name`.

---

## Setup

### 1. Create a virtual environment (recommended)

```bash
cd phase1/code
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

If the ingest script fails on `pd.read_csv`, install pandas:

```bash
pip install pandas
```

### 3. Configure Neo4j

Copy the example env and set your Neo4j credentials:

```bash
cp env.example .env
```

Edit `.env`:

```env
NEO4J_URI=neo4j://127.0.0.1:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DB=neo4j
```

### 4. Start Neo4j (if not already running)

- **Neo4j Desktop:** Start your database and ensure Bolt is on port 7687.
- **Docker:**
  ```bash
  docker run --name neo4j-movies -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:latest
  ```
- Open **Neo4j Browser** at http://localhost:7474 to inspect the graph.

---

## Folder Structure

```
phase1/
├── README.md                 # This file
├── data/
│   └── movie.csv             # Input dataset (movie_id, movie_name, year, overview, director, genre, cast)
└── code/
    ├── main.py                # Entry point: ingest movie.csv into Neo4j
    ├── requirements.txt
    ├── .env                   # Your config (not committed)
    ├── env.example            # Template for .env
    ├── core/
    │   └── config.py          # Settings from .env (Neo4j URI, user, password, db)
    ├── db/
    │   └── connection.py     # Neo4jConnection: execute() for writes, execute_query() for reads
    ├── graph/
    │   └── schema.py         # Cypher: constraints + MERGEs for Movie, Genre, Person, relationships
    ├── ingest/
    │   └── load_data.py      # Read CSV, validate with MovieModel, create graph
    ├── models/
    │   └── movie.py          # Pydantic MovieModel (validates rows, splits genre/cast)
    └── query/
        ├── __init__.py
        └── run.py            # Example Cypher queries run via db.execute_query()
```

---

## How to Run

All commands below are run from **`phase1/code`**.

### 1. Ingest data

Load the movie CSV into Neo4j (creates constraints, then Movie, Genre, Person nodes and relationships):

```bash
python main.py
```

Update the path in `main.py` if your `movie.csv` lives elsewhere (e.g. absolute path to `phase1/data/movie.csv`).

### 2. Run example queries

Use the query layer to run Cypher you write by hand:

```bash
python -c "from query.run import *"
```

Or open `query/run.py`, add or edit Cypher strings, and run it. Example pattern:

```python
from db.connection import Neo4jConnection
db = Neo4jConnection()
result = db.execute_query("MATCH (m:Movie) RETURN m.name, m.year LIMIT 5")
for row in result:
    print(dict(row))
db.close()
```

### 3. Explore in Neo4j Browser

At http://localhost:7474 run Cypher yourself, e.g.:

- `MATCH (m:Movie) RETURN m LIMIT 10`
- `MATCH (p:Person)-[:DIRECTED]->(m:Movie) RETURN p.name, m.name LIMIT 10`
- `MATCH (m:Movie)-[:HAS_GENRE]->(g:Genre) WHERE g.name = 'Drama' RETURN m.name LIMIT 10`

---

## Configuration

| Variable | Description |
|----------|-------------|
| `NEO4J_URI` | Neo4j Bolt URI (e.g. `neo4j://127.0.0.1:7687`) |
| `NEO4J_USER` | Neo4j user |
| `NEO4J_PASSWORD` | Neo4j password |
| `NEO4J_DB` | Database name (e.g. `neo4j`) |

---

## Security

- Do not commit `.env`; use `env.example` as a template.
- The ingest script creates nodes and relationships; the query layer is read-only by convention (you control the Cypher in `query/run.py`).

---

## Troubleshooting

| Issue | What to do |
|-------|------------|
| “Connection refused” to Neo4j | Start Neo4j and check `NEO4J_URI` and port 7687. |
| “Validation failed” during ingest | Check CSV columns match `MovieModel` in `models/movie.py` (movie_id, movie_name, year, overview, director, genre, cast). |
| `NameError: name 'pd' is not defined` | Install pandas: `pip install pandas`. |
| Constraint / uniqueness errors | Ensure `movie_id`, director/cast names, and genre strings are consistent; re-run ingest if you fixed the data. |

---

## Next: Phase 2

After Phase 1 is solid (ingest works, you can write and run Cypher by hand), move to **Phase 2** for natural language → Cypher using an LLM. See `../phase2/README.md`.
