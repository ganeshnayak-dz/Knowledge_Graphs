# Knowledge Graph — Learning & Development

A project to build **graph and Cypher skills**, then add **natural language → Cypher** (e.g. Groq), and eventually **hybrid graph + vector** search. The approach is step-by-step and interview-worthy: no shortcuts, proper engineering.

The full roadmap and checklist live in **[plan.md](plan.md)**. This README summarizes what the repo is about and how to run it.

---

## What This Repo Is About

| Phase | Goal | Status |
|-------|------|--------|
| **Phase 1** | Pure graph foundation: model data as a graph, ingest into Neo4j, write Cypher by hand. No LLM. | ✅ Implemented |
| **Phase 2** | Add an LLM (e.g. Groq) to translate natural language questions into Cypher and run them on the graph. | Planned |
| **Phase 3** | Advanced: combine graph with vector search (e.g. document chunks, PDF ingestion). | Planned |

**Dataset:** A **custom movie dataset** (`movie.csv`) — movie metadata with `movie_id`, `movie_name`, `year`, `overview`, `director`, `genre` (comma-separated), and `cast` (comma-separated). There are no user ratings; the graph is about **movies, genres, and people** (directors and actors).

---

## Phase 1 — What’s Implemented

Phase 1 focuses on:

- **Graph modeling** — Thinking in nodes and relationships instead of tables.
- **Neo4j** — Loading and querying the graph with Cypher.
- **Python pipeline** — CSV → validation (Pydantic) → Neo4j via the official driver.

### Graph Schema (Phase 1)

- **Nodes**
  - **Movie:** `movie_id`, `name`, `year`, `overview`
  - **Genre:** `name`
  - **Person:** `name` (used for both directors and actors)
- **Relationships**
  - `Movie -[:HAS_GENRE]-> Genre`
  - `Person -[:DIRECTED]-> Movie`
  - `Person -[:ACTED_IN]-> Movie`

Constraints ensure uniqueness on `Movie.movie_id`, `Person.name`, and `Genre.name`.

### Repository Layout (Phase 1)

```
Knowledge_graph/
├── plan.md                    # Full learning plan and phase checklist
├── README.md                  # This file
└── phase1/
    ├── requirements.txt      # Python dependencies
    ├── data/
    │   └── movie.csv         # Input dataset (movie_id, movie_name, year, overview, director, genre, cast)
    └── code/
        ├── main.py           # Entry point: runs ingest from movie.csv
        ├── core/
        │   └── config.py     # Settings from .env (Neo4j URI, user, password, db)
        ├── db/
        │   └── connection.py # Neo4jConnection: execute() for writes, execute_query() for reads
        ├── graph/
        │   └── schema.py     # Cypher: constraints + MERGEs for Movie, Genre, Person, relationships
        ├── ingest/
        │   └── load_data.py  # Read CSV, validate with MovieModel, create graph (constraints + nodes/rels)
        ├── models/
        │   └── movie.py      # Pydantic MovieModel for row validation
        └── query/            # Query layer (Cypher constants + run helpers)
            ├── __init__.py
            └── run.py        # Functions that run read queries via db.execute_query()
```

---

## Setup and Run (Phase 1)

### Prerequisites

- **Python 3.x** (3.10+ recommended)
- **Neo4j** (Desktop or Docker), running and reachable

### 1. Install Neo4j

- **Option A:** [Neo4j Desktop](https://neo4j.com/download/)
- **Option B (Docker):**
  ```bash
  docker run --name neo4j-movies -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:latest
  ```
- Open Neo4j Browser at **http://localhost:7474** to inspect the graph.

### 2. Clone and Python environment

```bash
cd Knowledge_graph/phase1
pip install -r requirements.txt
```

Dependencies: `neo4j`, `pandas`, `pydantic`, `pydantic-settings`, `python-dotenv`.

### 3. Configure Neo4j

In `phase1/code/`, copy the example env and fill in your Neo4j credentials:

```bash
cd phase1/code
copy env.example .env
```

Edit `.env` with:

- `NEO4J_URI` (e.g. `bolt://localhost:7687`)
- `NEO4J_USER` (e.g. `neo4j`)
- `NEO4J_PASSWORD`
- `NEO4J_DB` (e.g. `neo4j`)

### 4. Run the ingest

From `phase1/code/` (so that imports like `db.connection` and `graph.schema` work):

```bash
python main.py
```

`main.py` calls `ingest_movies()` with the path to `phase1/data/movie.csv`. The pipeline:

1. Creates constraints (Movie, Person, Genre).
2. For each CSV row: validates with `MovieModel`, then creates the Movie node, HAS_GENRE to Genre(s), DIRECTED from director Person, ACTED_IN from each cast Person.

### 5. Verify in Neo4j Browser

Run in the Neo4j Browser:

```cypher
MATCH (n) RETURN labels(n), count(n);
MATCH ()-[r]->() RETURN type(r), count(r);
```

You should see counts for `Movie`, `Genre`, `Person` and for `HAS_GENRE`, `DIRECTED`, `ACTED_IN`.

---

## Example Cypher Queries (Phase 1)

You can run these in **Neo4j Browser** or via the Python **query** layer using `db.execute_query()`.

- **Movies in a genre**
  ```cypher
  MATCH (m:Movie)-[:HAS_GENRE]->(g:Genre {name: "Drama"}) RETURN m.name, m.year ORDER BY m.year DESC;
  ```
- **Movies by director**
  ```cypher
  MATCH (p:Person)-[:DIRECTED]->(m:Movie) WHERE p.name = $name RETURN m.name, m.year;
  ```
- **Co-actors (who acted in the same movies as a given person)**
  ```cypher
  MATCH (a:Person)-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(b:Person)
  WHERE a.name = $name AND a <> b
  RETURN b.name, count(m) AS sharedMovies ORDER BY sharedMovies DESC LIMIT 10;
  ```
- **Node and relationship counts**
  ```cypher
  MATCH (n) RETURN labels(n)[0] AS label, count(n) AS cnt ORDER BY cnt DESC;
  MATCH ()-[r]->() RETURN type(r) AS relType, count(r) AS cnt ORDER BY cnt DESC;
  ```

More query ideas (by genre, director, cast, aggregates) are in **[plan.md](plan.md)** (Step 6 and the 15 example questions).

---

## Roadmap (from plan.md)

- **Phase 1:** No LLM — master the graph schema and Cypher; ingest and query the movie graph. *(Current.)*
- **Phase 2:** Add Groq (or another LLM) for natural language → Cypher; validate and run generated queries; simple CLI or API.
- **Phase 3:** Hybrid graph + vector (e.g. document chunks, PDF ingestion); combine graph traversal with vector similarity.

Details and checklists for each phase are in **[plan.md](plan.md)**.

---

## License and Contributing

Use this repo for learning and development. For the exact learning plan, success criteria, and step-by-step checklist, see **[plan.md](plan.md)**.
