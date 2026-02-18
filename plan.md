# Knowledge Graph — Learning & Development Plan

**Purpose:** Build graph and Cypher skills, then add NL→Cypher (Groq), then hybrid graph+vector. No shortcuts — proper engineering, interview-worthy.

**Dataset:** MovieLens small (movies, ratings; optionally tags, links later).  
*If switching to HR dataset, schema design will be analogous.*

---

## Phase 1 — No LLM (Pure Graph Foundation)

**Goal:** Understand graph modeling, learn Cypher, think in relationships, build something interview-worthy.

### Step 0 — Setup Environment

- [ ] **Install Neo4j**
  - Option A: [Neo4j Desktop](https://neo4j.com/download/) (easiest for beginner)
  - Option B: Docker (better for backend mindset):

    ```bash
    docker run --name neo4j-movies -p7474:7474 -p7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:latest
    ```

- [ ] Open Neo4j Browser: `http://localhost:7474`

### Step 1 — Download Dataset

- [ ] Get [MovieLens small](https://grouplens.org/datasets/movielens/) from GroupLens Research
- [ ] Use at minimum: `movies.csv`, `ratings.csv`  
  *(Optional later: tags.csv, links.csv)*

### Step 2 — Understand Raw CSV Structure

**Core entities (answer before importing):**

- **movies.csv:** `movieId`, `title`, `genres` (pipe-separated)
- **ratings.csv:** `userId`, `movieId`, `rating`, `timestamp`

### Step 3 — Design Graph Schema

**Nodes:** `User`, `Movie`, `Genre`  
**Relationships:** `User -[:RATED]-> Movie`, `Movie -[:HAS_GENRE]-> Genre`

*Graph schema = meaning (entities + relationships), not columns/tables.*

### Step 4 — Prepare Data for Import

- [ ] Place CSVs in Neo4j import folder  
  Docker:  
  `docker cp movies.csv neo4j-movies:/var/lib/neo4j/import/`  
  `docker cp ratings.csv neo4j-movies:/var/lib/neo4j/import/`

### Step 5 — Import Movies

- [ ] In Neo4j Browser, run:

  ```cypher
  LOAD CSV WITH HEADERS FROM 'file:///movies.csv' AS row
  MERGE (m:Movie {movieId: toInteger(row.movieId)})
  SET m.title = row.title
  ```

- [ ] Verify: `MATCH (m:Movie) RETURN count(m);`

### Step 6 — Create Genres

- [ ] Split pipe-separated genres and link to movies:

  ```cypher
  LOAD CSV WITH HEADERS FROM 'file:///movies.csv' AS row
  WITH row, split(row.genres, "|") AS genres
  MATCH (m:Movie {movieId: toInteger(row.movieId)})
  UNWIND genres AS genre
  MERGE (g:Genre {name: genre})
  MERGE (m)-[:HAS_GENRE]->(g);
  ```

- [ ] Test: `MATCH (g:Genre) RETURN g;`

### Step 7 — Import Users + Ratings

- [ ] Run:

  ```cypher
  LOAD CSV WITH HEADERS FROM 'file:///ratings.csv' AS row
  MERGE (u:User {userId: toInteger(row.userId)})
  MERGE (m:Movie {movieId: toInteger(row.movieId)})
  MERGE (u)-[r:RATED]->(m)
  SET r.rating = toFloat(row.rating);
  ```

### Step 8 — Explore the Graph

- [ ] Count nodes: `MATCH (n) RETURN labels(n), count(n);`
- [ ] Count relationships: `MATCH ()-[r]->() RETURN type(r), count(r);`

### Step 9 — Write Real Cypher Queries (Critical)

- [ ] **Top rated movies:**  
  `MATCH (u:User)-[r:RATED]->(m:Movie) RETURN m.title, avg(r.rating) AS avgRating ORDER BY avgRating DESC LIMIT 10;`
- [ ] **Users who like same movies (multi-hop):**  
  `MATCH (u1:User)-[:RATED]->(m:Movie)<-[:RATED]-(u2:User) WHERE u1.userId = 1 AND u1 <> u2 RETURN u2.userId, count(m) AS commonMovies ORDER BY commonMovies DESC;`
- [ ] **Recommend movies (graph-based):**  
  `MATCH (u:User {userId: 1})-[:RATED]->(m1:Movie) MATCH (m1)<-[:RATED]-(other:User)-[:RATED]->(m2:Movie) WHERE NOT (u)-[:RATED]->(m2) RETURN m2.title, count(*) AS score ORDER BY score DESC LIMIT 5;`
- [ ] **Target:** 10–15 Cypher queries; practice recommendation logic

### Step 10 — Add Constraints (Professional)

- [ ] Run:

  ```cypher
  CREATE CONSTRAINT user_unique IF NOT EXISTS FOR (u:User) REQUIRE u.userId IS UNIQUE;
  CREATE CONSTRAINT movie_unique IF NOT EXISTS FOR (m:Movie) REQUIRE m.movieId IS UNIQUE;
  ```

### Phase 1 Deliverables

- [ ] Neo4j running with MovieLens data loaded
- [ ] Schema: User, Movie, Genre + RATED, HAS_GENRE
- [ ] 10–15 Cypher queries (incl. top rated, similar users, recommendations)
- [ ] Constraints on `User.userId` and `Movie.movieId`
- [ ] README documenting setup, schema, and example queries

### Phase 1 — DO NOT

- No Groq / no LLM
- No PDFs, no vector DB
- First master Cypher

### Suggested Timeline (Phase 1)

- **Day 1:** Setup + dataset + import (Steps 0–7)
- **Day 2:** Explore graph + write 15 Cypher queries + recommendation logic (Steps 8–9)
- **Day 3:** Constraints, clean-up, export README (Step 10 + docs)

---

## Phase 2 — Add Groq (NL → Cypher)

**Goal:** Natural language → Cypher; validate generated queries.

- [ ] Integrate Groq (or chosen LLM) to translate user questions to Cypher
- [ ] Validate/sanitize generated Cypher before execution
- [ ] Expose a simple interface (CLI or minimal API) for “ask in English, run on graph”

*Start only after Phase 1 is solid (10–15 queries written by hand).*

---

## Phase 3 — Advanced (Hybrid Graph + Vector)

**Goal:** Combine graph with vector search; PDF ingestion.

- [ ] Add vector store (e.g. for document chunks)
- [ ] PDF ingestion pipeline
- [ ] Hybrid: graph traversal + vector similarity where appropriate

*Start only after Phase 2 NL→Cypher is working.*

---

## Success Criteria (Phase 1)

By end of Phase 1 you should be able to:

- Model entities and relationships in graph terms
- Traverse the graph (single and multi-hop)
- Aggregate over paths (avg, count, recommendations)
- Explain how graph thinking differs from SQL
- Confidently write 10–15 Cypher queries

Then proceed to Phase 2 (NL → Cypher with Groq).
