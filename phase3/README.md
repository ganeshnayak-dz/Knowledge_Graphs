# Phase 3 — Graph Engineering (Strengthen Foundation)

**Goal:** Think like a graph architect; write efficient, explainable queries.

**Suggested duration:** ~2 weeks.

---

## Overview

| Section | Focus | Outcome |
|--------|--------|---------|
| **3.1** | Advanced graph modeling | Two domain graphs + constraints/indexes |
| **3.2** | Query optimization & profiling | EXPLAIN/PROFILE, interpret plans, document 2–3 optimizations |

**Deliverable:** Document 2–3 optimizations (e.g. index added, query rewritten). See [Deliverable](#deliverable) at the end.

---

## 3.1 Advanced Graph Modeling

### What you need to learn (in order)

Work through each topic below. Use the references to read/watch, then tick the box when you can explain or apply it.

---

#### Topic 1: Labels vs relationship types

- [ ] **When to use labels**
  - Labels categorize **nodes** (e.g. `:Person`, `:Movie`, `:Department`). Use them for entity types, indexing, and constraining uniqueness.
  - One node can have multiple labels (e.g. `:Person:Employee`).
- [ ] **When to use relationship types**
  - Relationship types describe **how** two nodes are connected (e.g. `WORKS_IN`, `ACTED_IN`, `HAS_GENRE`). They are first-class in Cypher and affect traversal and indexing.
- [ ] **Rule of thumb:** Labels = “what is this node?”; Relationship types = “how are these two nodes related?”

| Reference | Type | Link |
|-----------|------|------|
| Graph Modeling: Labels | Article (Neo4j) | [Medium — Graph Modeling: Labels](https://medium.com/neo4j/graph-modeling-labels-71775ff7d121) |
| Cypher Manual — Nodes and relationships | Docs | [Neo4j Docs — Graph database concepts](https://neo4j.com/docs/cypher-manual/current/clauses/create/#create-create-nodes-and-relationships) |

---

#### Topic 2: Property modeling

- [ ] **Which properties belong on nodes vs relationships**
  - Node properties: identity and attributes of the entity (e.g. `name`, `year`, `salary`).
  - Relationship properties: attributes of the **connection** (e.g. `since`, `role`, `quantity`).
- [ ] **Avoid storing large or frequently changing blobs on nodes** if you need to filter or aggregate; prefer references or separate nodes.
- [ ] **Naming:** Use consistent, query-friendly names (e.g. `created_at` vs `creationDate` — pick one style).

| Reference | Type | Link |
|-----------|------|------|
| Best Practices for Neo4j Data Modeling | Article | [Neo4j Guide — Data Modeling Best Practices](https://neo4j.guide/article/Best_Practices_for_Neo4j_Data_Modeling.html) |
| Graph Data Modeling Fundamentals | Course (Graph Academy) | [Graph Academy — Modeling Fundamentals](https://graphacademy.neo4j.com/courses/modeling-fundamentals/) |

---

#### Topic 3: Avoiding supernodes

- [ ] **What is a supernode**
  - A node with a very high number of relationships (often 100k+), e.g. one “Genre” node connected to millions of movies, or one “User” with millions of follows.
- [ ] **Why they hurt**
  - Traversals from that node touch many relationships; MERGE/expand can become slow; planner may not use indexes well.
- [ ] **How to avoid or mitigate**
  - **Modeling:** Introduce intermediate nodes (e.g. year or category nodes) to “fan out” instead of one huge hub.
  - **Queries:** Always specify relationship type and direction so the engine doesn’t scan all relationships.
  - **Optional:** Relationship type indexes / composite patterns; in extreme cases, partition (e.g. by time or category).

| Reference | Type | Link |
|-----------|------|------|
| Graph Modeling: All About Super Nodes | Article (Neo4j) | [Medium — Super Nodes](https://medium.com/neo4j/graph-modeling-all-about-super-nodes-d6ad7e11015b) |
| Neo4j Community — Super nodes | Discussion | [Community — Super Nodes](https://community.neo4j.com/t/graph-modeling-all-about-super-nodes/27464) |
| Super Node Performance | Blog | [Justin Boylan-Toomey — Super Node Performance](https://www.jboylantoomey.com/post/neo4j-super-node-performance-issues) |

---

#### Topic 4: Many-to-many and intermediate nodes

- [ ] **Many-to-many in graphs**
  - Natural in graphs: e.g. Person–(ACTED_IN)–Movie, Employee–(WORKS_ON)–Project. Use a relationship (and optional relationship properties) or an intermediate node.
- [ ] **When to use an intermediate node**
  - When the link itself has important attributes or lifecycle (e.g. “assignment” with `role`, `start_date`, `end_date`) or when you need to connect more facts to the participation (e.g. Assignment–(REPORTED_TO)–Manager).

| Reference | Type | Link |
|-----------|------|------|
| Graph Data Modeling Fundamentals | Course | [Graph Academy — Modeling Fundamentals](https://graphacademy.neo4j.com/courses/modeling-fundamentals/) (covers intermediate nodes, refactoring) |

---

#### Topic 5: Temporal modeling (valid_from, valid_to)

- [ ] **Time-bounded facts**
  - For “X was true from date A to date B”, store `valid_from` and `valid_to` (or `start_date`, `end_date`) on the relationship (or node).
- [ ] **Current state**
  - Use `valid_to = null` (or a sentinel like “infinity”) for “currently valid”. Filter in Cypher: `WHERE r.valid_to IS NULL OR r.valid_to > date()`.
- [ ] **Neo4j temporal types**
  - Use `date()`, `datetime()` for consistency; Cypher supports DATE, ZONED DATETIME, DURATION.

| Reference | Type | Link |
|-----------|------|------|
| Temporal Versioning in Neo4j | Article | [DEV — Temporal Versioning in Neo4j](https://dev.to/satyam_shree_087caef77512/a-practical-guide-to-temporal-versioning-in-neo4j-nodes-relationships-and-historical-graph-1m5g) |
| Data model for relationships in time | Community | [Neo4j Community — Relationships in Time](https://community.neo4j.com/t/data-model-for-relationships-in-time/49715) |
| Temporal values — Cypher Manual | Docs | [Neo4j Docs — Temporal values](https://neo4j.com/docs/cypher-manual/current/values-and-types/temporal/) |

---

#### Task: Build two small domain graphs

Do both; by hand (Cypher in Neo4j Browser) or via a small Python ingest (similar to Phase 1).

---

**Graph 1: Employee–Project–Department**

- [ ] **Nodes**
  - `Employee` (e.g. `name`, `employee_id`, `hire_date`)
  - `Department` (e.g. `name`, `department_id`)
  - `Project` (e.g. `name`, `project_id`, `start_date`, `end_date`)
- [ ] **Relationships**
  - `(Employee)-[:WORKS_IN]->(Department)`
  - `(Employee)-[:WORKS_ON {role?, allocation?, from?, to?}]->(Project)` (add properties if you want temporal assignment)
- [ ] **Constraints**
  - Uniqueness on `Employee.employee_id`, `Department.department_id`, `Project.project_id` (or equivalent).
- [ ] **Indexes**
  - Index the properties you use in `WHERE` or `MATCH` (e.g. `employee_id`, `name`).

---

**Graph 2: E-commerce — Product–Order–User**

- [ ] **Nodes**
  - `User` (e.g. `user_id`, `email`, `name`)
  - `Product` (e.g. `product_id`, `name`, `price`, `category`)
  - `Order` (e.g. `order_id`, `created_at`, `status`, `total`)
- [ ] **Relationships**
  - `(User)-[:PLACED]->(Order)`
  - `(Order)-[:CONTAINS {quantity, unit_price}]->(Product)` (line items as relationship with quantity/price)
- [ ] **Constraints**
  - Uniqueness on `User.user_id`, `Product.product_id`, `Order.order_id`.
- [ ] **Indexes**
  - Index lookup keys and any property you filter on (e.g. `Order.created_at`, `Product.category`).

---

#### Task: Constraints, indexes, and unique keys

- [ ] **Constraints**
  - Use `CREATE CONSTRAINT ... FOR (n:Label) REQUIRE n.prop IS UNIQUE` (or equivalent) for natural keys so duplicates are impossible.
- [ ] **Indexes**
  - Create indexes for properties used in `WHERE`, `MATCH`, and joins: `CREATE INDEX [name] FOR (n:Label) ON (n.prop)`.
  - Check: `SHOW INDEXES` / `SHOW CONSTRAINTS` in Neo4j.
- [ ] **Docs**
  - [Neo4j — Create indexes](https://neo4j.com/docs/cypher-manual/current/indexes/search-performance-indexes/create-indexes/)
  - [Neo4j — Constraints](https://neo4j.com/docs/cypher-manual/current/constraints/)

---

## 3.2 Query Optimization & Profiling

### What you need to learn (in order)

---

#### Topic 1: EXPLAIN and PROFILE in Neo4j

- [ ] **EXPLAIN**
  - Shows the **planned** execution without running the query. No result rows, no DB writes. Use to see which indexes and operators the planner chose.
- [ ] **PROFILE**
  - **Runs** the query and shows the same plan plus **actual metrics**: rows per operator, db hits, time. Use only when tuning (it has overhead).
- [ ] **How to run**
  - In Neo4j Browser or any driver: prefix your query with `EXPLAIN` or `PROFILE`, e.g. `PROFILE MATCH (m:Movie) RETURN m.name LIMIT 10`.

| Reference | Type | Link |
|-----------|------|------|
| Execution plans and query tuning | Docs | [Neo4j — Planning and tuning](https://neo4j.com/docs/cypher-manual/current/planning-and-tuning/) |
| How to profile a query | Docs | [Neo4j — How do I profile a query](https://neo4j.com/docs/cypher-manual/4.0/query-tuning/how-do-i-profile-a-query/) |
| Understanding execution plans | Docs | [Neo4j — Execution plans](https://neo4j.com/docs/cypher-manual/current/planning-and-tuning/execution-plans/) |
| How to get execution plans (EXPLAIN/PROFILE) | Support | [Neo4j Support — EXPLAIN and PROFILE](https://support.neo4j.com/s/article/6638160188691-How-to-get-Cypher-query-execution-plans-using-EXPLAIN-and-PROFILE) |

---

#### Topic 2: Query plans, index usage, cardinality, bottlenecks

- [ ] **Execution plan**
  - A tree of operators (e.g. NodeIndexSeek, Expand, Filter, Limit). Bottom = data access; top = result. Read from bottom up to see “where the work happens.”
- [ ] **Index usage**
  - Look for `NodeIndexSeek`, `NodeUniqueIndexSeek` in the plan. If you see full scans (`NodeByLabelScan`) on large labels, consider adding or using an index.
- [ ] **Cardinality**
  - Number of rows flowing between operators. High cardinality early (e.g. before a Filter) often means unnecessary work; filter as early as possible.
- [ ] **Bottlenecks**
  - High “db hits” or “rows” on one operator; many rows going into an Expand from a dense node; no index on the starting point.

| Reference | Type | Link |
|-----------|------|------|
| Understanding Cypher cardinality | KB | [Neo4j KB — Understanding Cypher cardinality](https://neo4j.com/developer/kb/understanding-cypher-cardinality/) |
| Tuning Cypher: tips and tricks | Blog | [Neo4j Blog — Tuning Cypher](https://neo4j.com/blog/tuning-cypher-queries/) |

---

#### Task: Run EXPLAIN/PROFILE on Phase 1 queries

- [ ] Pick **3–5** Cypher queries from Phase 1 (movie graph: by genre, director, co-actors, aggregates). If you don’t have them in code, take them from your Neo4j Browser history or from `phase1/README.md` examples.
- [ ] Run each with `EXPLAIN`, then with `PROFILE`.
- [ ] For each query, note:
  - Which operator has the most rows or db hits?
  - Is an index used for the starting label/property?
  - Where does cardinality grow (e.g. after a variable-length path)?
- [ ] Write 1–2 sentences per query: “What the plan shows and one possible improvement.”

---

#### Task: Document 2–3 optimizations (deliverable)

- [ ] Apply **2–3** concrete optimizations. For each, document:
  - **Before:** query (or snippet) and what PROFILE showed (e.g. “NodeByLabelScan on Movie, 50k db hits”).
  - **Change:** e.g. “Added index on `Movie(movie_id)` and used it in MATCH” or “Moved WHERE genre into the first MATCH and added LIMIT.”
  - **After:** what PROFILE showed (e.g. “NodeIndexSeek, 10 db hits”) or “rows reduced from X to Y.”
- [ ] Save this in a short doc (e.g. `phase3/OPTIMIZATIONS.md` or a section in this README). That is your Phase 3 deliverable.

---

## Deliverable

- **2–3 optimizations** documented with:
  - Before (query + PROFILE observation),
  - Change (index added / query rewritten),
  - After (PROFILE or row-count improvement).

Optionally, also keep:
- Notes from the two domain graphs (schema + sample Cypher for constraints/indexes).
- Your EXPLAIN/PROFILE notes for the 3–5 Phase 1 queries.

---

## References summary

### Official Neo4j documentation

| Topic | URL |
|-------|-----|
| Planning and tuning (EXPLAIN, PROFILE) | https://neo4j.com/docs/cypher-manual/current/planning-and-tuning/ |
| Execution plans | https://neo4j.com/docs/cypher-manual/current/planning-and-tuning/execution-plans/ |
| Create indexes | https://neo4j.com/docs/cypher-manual/current/indexes/search-performance-indexes/create-indexes/ |
| Constraints | https://neo4j.com/docs/cypher-manual/current/constraints/ |
| Temporal values (date, datetime) | https://neo4j.com/docs/cypher-manual/current/values-and-types/temporal/ |

### Articles & blogs

| Topic | URL |
|-------|-----|
| Graph modeling: Labels | https://medium.com/neo4j/graph-modeling-labels-71775ff7d121 |
| Graph modeling: Super nodes | https://medium.com/neo4j/graph-modeling-all-about-super-nodes-d6ad7e11015b |
| Best practices: Data modeling | https://neo4j.guide/article/Best_Practices_for_Neo4j_Data_Modeling.html |
| Temporal versioning in Neo4j | https://dev.to/satyam_shree_087caef77512/a-practical-guide-to-temporal-versioning-in-neo4j-nodes-relationships-and-historical-graph-1m5g |
| Tuning Cypher queries | https://neo4j.com/blog/tuning-cypher-queries/ |
| Understanding Cypher cardinality (KB) | https://neo4j.com/developer/kb/understanding-cypher-cardinality/ |

### Courses (free, self-paced)

| Course | Duration | URL |
|--------|----------|-----|
| Graph Data Modeling Fundamentals | ~2 hours | https://graphacademy.neo4j.com/courses/modeling-fundamentals/ |
| Cypher Fundamentals | ~1 hour | https://graphacademy.neo4j.com/courses/cypher-fundamentals/ |
| Intermediate Cypher Queries | ~4 hours | https://graphacademy.neo4j.com/courses/cypher-intermediate-queries |
| Cypher Patterns (advanced) | — | https://graphacademy.neo4j.com/courses/cypher-patterns/ |

### Community & support

| Resource | URL |
|----------|-----|
| Neo4j Community (modeling, supernodes, temporal) | https://community.neo4j.com/ |
| How to get EXPLAIN/PROFILE plans | https://support.neo4j.com/s/article/6638160188691-How-to-get-Cypher-query-execution-plans-using-EXPLAIN-and-PROFILE |

---

## Checklist (Phase 3 at a glance)

**3.1 Advanced graph modeling**

- [ ] Labels vs relationship types (read + apply)
- [ ] Property modeling (read + apply)
- [ ] Avoiding supernodes (read + apply)
- [ ] Many-to-many and intermediate nodes (read + apply)
- [ ] Temporal modeling valid_from / valid_to (read + apply)
- [ ] Graph 1: Employee–Project–Department (nodes, relationships, constraints, indexes)
- [ ] Graph 2: E-commerce Product–Order–User (nodes, relationships, constraints, indexes)
- [ ] Constraints and indexes created and verified (`SHOW INDEXES`, `SHOW CONSTRAINTS`)

**3.2 Query optimization & profiling**

- [ ] EXPLAIN vs PROFILE (when to use each)
- [ ] Read execution plans (operators, index usage, cardinality)
- [ ] Run EXPLAIN/PROFILE on 3–5 Phase 1 Cypher queries; interpret and note improvements
- [ ] Document 2–3 optimizations (before / change / after) — **deliverable**

---

**Next:** After Phase 3, proceed to [Phase 4 — Graph Intelligence](../plan.md#phase-4--graph-intelligence-algorithms) (GDS algorithms: PageRank, paths, community detection).
