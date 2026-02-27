# Phase 3 — Plan: Graph Engineering (Strengthen Foundation)

**Goal:** Think like a graph architect. Learn advanced modeling patterns, write efficient queries, profile and optimize them. By the end you should be able to design a graph schema for any domain and justify your choices.

**Duration:** ~2 weeks.

**Prerequisites:**
- Phase 1 complete (movie graph in Neo4j with Movie, Genre, Person nodes).
- Phase 2 complete (employee graph with Department, Position; NL→Cypher pipeline).
- Comfortable writing basic Cypher (MATCH, MERGE, WHERE, WITH, RETURN).

**Deliverables:**
1. Two new domain graphs (Employee–Project–Department, E-commerce) with constraints and indexes.
2. EXPLAIN/PROFILE notes for 3–5 Phase 1 queries.
3. 2–3 documented optimizations in `OPTIMIZATIONS.md` (before / change / after).

---

## Week 1: Advanced Graph Modeling (Section 3.1)

### Day 1–2: Learn the Five Modeling Topics

Read the references below (linked in `README.md` too). For each topic, the goal is: **read → understand → be able to explain it in your own words → apply it**.

---

#### Topic 1: Labels vs Relationship Types

**What to learn:**
- Labels categorize nodes (`:Person`, `:Movie`, `:Department`). Think of them as "what is this thing?"
- Relationship types describe connections (`ACTED_IN`, `WORKS_IN`, `HAS_GENRE`). Think of them as "how are these two things related?"
- One node can have multiple labels (e.g., `:Person:Director`).
- Relationship types are first-class in Cypher — they affect traversal performance and pattern matching.

**Apply to your existing graphs:**
- Look at your Phase 1 movie graph. Are `Person` nodes that are directors and actors modeled correctly? Should you add a `:Director` or `:Actor` label, or is the relationship type (`DIRECTED` vs `ACTED_IN`) sufficient?
- Answer: The relationship type is usually better (a person can be both actor and director), but adding labels can speed up filtered queries like `MATCH (d:Director)` instead of scanning all `:Person` nodes.

**Exercise:**
- [ ] In Neo4j Browser, run: `MATCH (p:Person)-[:DIRECTED]->() RETURN DISTINCT p.name LIMIT 10` and then try what it would look like if you had a `:Director` label. Think about when each approach is better.

**References:**
- [Graph Modeling: Labels](https://medium.com/neo4j/graph-modeling-labels-71775ff7d121)
- [Neo4j Docs — Nodes and relationships](https://neo4j.com/docs/cypher-manual/current/clauses/create/)

---

#### Topic 2: Property Modeling

**What to learn:**
- **Node properties:** Identity and attributes of the entity (`name`, `year`, `salary`).
- **Relationship properties:** Attributes of the connection (`since`, `role`, `quantity`). Use these when the attribute belongs to the *link*, not the entity.
- Avoid storing large blobs on nodes if you need to filter/aggregate — prefer references or separate nodes.
- Pick a naming convention and stick with it (e.g., `snake_case` for all properties).

**Apply to your existing graphs:**
- Phase 1: `Movie.overview` is a large text blob. Is it appropriate on the node? (Yes, for now — but in a production system you might store it separately or in a vector store.)
- Phase 2: `Employee.salary` is on the Employee node. If salary changes over time, should it be on a relationship to a `SalaryRecord` node instead?

**Exercise:**
- [ ] Pick 3 properties from your movie or employee graph. For each, write one sentence: "This property is on [node/relationship] because [reason]."

**References:**
- [Best Practices for Neo4j Data Modeling](https://neo4j.guide/article/Best_Practices_for_Neo4j_Data_Modeling.html)
- [Graph Academy — Modeling Fundamentals](https://graphacademy.neo4j.com/courses/modeling-fundamentals/)

---

#### Topic 3: Avoiding Supernodes

**What to learn:**
- A **supernode** is a node with an extremely high number of relationships (100k+). Example: a `:Genre` node like "Action" connected to 500,000 movies.
- Traversals from a supernode are slow because the engine must scan all its relationships.
- **Mitigation strategies:**
  - Introduce intermediate nodes to fan out (e.g., `Genre → Year → Movie` instead of `Genre → Movie`).
  - Always specify relationship type AND direction in queries.
  - In extreme cases: partition by time or category.

**Apply to your movie graph:**
- Run this in Neo4j Browser to check which nodes have the most relationships:
  ```cypher
  MATCH (n)
  WITH n, size([(n)--() | 1]) AS degree
  ORDER BY degree DESC
  LIMIT 10
  RETURN labels(n), n.name, degree
  ```
- Are any nodes approaching supernode territory? (With 2200 movies, probably not yet, but think about what would happen at 1M movies.)

**Exercise:**
- [ ] Run the degree query above. Note the top 5 nodes and their degree.
- [ ] For the highest-degree node, sketch (on paper or in a comment) how you would refactor it if the dataset grew 100x.

**References:**
- [Graph Modeling: All About Super Nodes](https://medium.com/neo4j/graph-modeling-all-about-super-nodes-d6ad7e11015b)
- [Super Node Performance](https://www.jboylantoomey.com/post/neo4j-super-node-performance-issues)

---

#### Topic 4: Many-to-Many and Intermediate Nodes

**What to learn:**
- Many-to-many is natural in graphs: `Person–(ACTED_IN)–Movie` is already M:N.
- When the **connection itself** has rich attributes (role, dates, allocation %), consider an intermediate node.
- Example: instead of `(Employee)-[:WORKS_ON {role, start, end}]->(Project)`, you could model `(Employee)-[:HAS_ASSIGNMENT]->(Assignment)-[:FOR_PROJECT]->(Project)` if the assignment has its own lifecycle (approved_by, status, etc.).

**Rule of thumb:** If the relationship has 3+ properties or needs to connect to other nodes, promote it to an intermediate node.

**Exercise:**
- [ ] Look at the E-commerce graph you'll build (Graph 2). The `CONTAINS` relationship between Order and Product has `quantity` and `unit_price`. Is a relationship sufficient, or should you use an intermediate `LineItem` node? Write your reasoning.

**References:**
- [Graph Academy — Modeling Fundamentals](https://graphacademy.neo4j.com/courses/modeling-fundamentals/) (covers intermediate nodes and refactoring)

---

#### Topic 5: Temporal Modeling (valid_from / valid_to)

**What to learn:**
- For time-bounded facts ("X was true from date A to date B"), store `valid_from` and `valid_to` on the relationship or node.
- Use `valid_to = null` for "currently valid." Filter: `WHERE r.valid_to IS NULL OR r.valid_to > date()`.
- Neo4j temporal types: `date()`, `datetime()`, `duration()`.

**Apply to your employee graph:**
- An employee's department can change over time. Instead of one `WORKS_IN` relationship, you could have multiple `WORKS_IN` relationships with `{from: date("2020-01-15"), to: date("2023-06-30")}` and the current one with `{from: date("2023-07-01"), to: null}`.

**Exercise:**
- [ ] Write a Cypher statement that creates an Employee with two `WORKS_IN` relationships to different departments at different time periods.
- [ ] Write a query that finds "current department" (where `to IS NULL`).

**References:**
- [Temporal Versioning in Neo4j](https://dev.to/satyam_shree_087caef77512/a-practical-guide-to-temporal-versioning-in-neo4j-nodes-relationships-and-historical-graph-1m5g)
- [Neo4j Docs — Temporal values](https://neo4j.com/docs/cypher-manual/current/values-and-types/temporal/)

---

### Day 3–4: Build Domain Graph 1 — Employee–Project–Department

**Context:** You already have the employee dataset from Phase 2 (`phase2/data/employee.csv`). This graph extends it with Projects.

#### Step 1: Create the dataset

Create a small `projects.csv` (put it in `phase3/data/` or `phase2/data/`):

```csv
project_id,project_name,start_date,end_date,department
P001,Website Redesign,2024-01-15,2024-06-30,IT
P002,Q1 Marketing Campaign,2024-02-01,2024-04-30,Marketing
P003,Data Migration,2024-03-01,2024-09-30,IT
P004,Employee Engagement Survey,2024-01-10,2024-03-15,HR
P005,Product Launch Alpha,2024-04-01,2024-12-31,Marketing
P006,Security Audit,2024-05-01,2024-07-31,IT
P007,Annual Report,2024-06-01,2024-08-31,Finance
P008,Customer Feedback Analysis,2024-03-15,2024-06-15,Operations
```

Create an `assignments.csv` to link employees to projects:

```csv
employee_name,project_id,role,allocation_pct,from_date,to_date
Douglas Lindsey,P002,Lead,80,2024-02-01,2024-04-30
Anthony Roberson,P003,Manager,50,2024-03-01,
Thomas Miller,P001,Developer,100,2024-01-15,2024-06-30
Thomas Miller,P003,Developer,60,2024-03-01,2024-09-30
Joshua Lewis,P002,Intern,100,2024-02-15,2024-04-30
```

(Pick 10–15 assignments using real names from `employee.csv`.)

#### Step 2: Design the schema

**Nodes:**
- `Employee` — `{name, age, gender, salary, ...}` (already exists from Phase 2)
- `Department` — `{department}` (already exists from Phase 2)
- `Position` — `{position}` (already exists from Phase 2)
- `Project` — `{project_id, name, start_date, end_date}` (NEW)

**Relationships:**
- `(Employee)-[:WORKS_IN]->(Department)` (existing)
- `(Employee)-[:HAS_ROLE]->(Position)` (existing)
- `(Employee)-[:WORKS_ON {role, allocation_pct, from_date, to_date}]->(Project)` (NEW — temporal + properties)
- `(Project)-[:BELONGS_TO]->(Department)` (NEW)

**Constraints:**
```cypher
CREATE CONSTRAINT project_id IF NOT EXISTS
FOR (p:Project) REQUIRE p.project_id IS UNIQUE
```

**Indexes:**
```cypher
CREATE INDEX project_name IF NOT EXISTS FOR (p:Project) ON (p.name)
CREATE INDEX project_start IF NOT EXISTS FOR (p:Project) ON (p.start_date)
```

#### Step 3: Ingest and verify

- Write a small Python script (or do it in Neo4j Browser) that reads `projects.csv` and `assignments.csv`, runs MERGE queries.
- Verify: `SHOW CONSTRAINTS`, `SHOW INDEXES`.
- Run sample queries:
  ```cypher
  // All projects in the IT department
  MATCH (p:Project)-[:BELONGS_TO]->(d:Department {department: "IT"}) RETURN p.name, p.start_date

  // Employees currently on any project (to_date IS NULL)
  MATCH (e:Employee)-[w:WORKS_ON]->(p:Project)
  WHERE w.to_date IS NULL
  RETURN e.name, p.name, w.role

  // Employees working on more than one project
  MATCH (e:Employee)-[:WORKS_ON]->(p:Project)
  WITH e, count(p) AS proj_count
  WHERE proj_count > 1
  RETURN e.name, proj_count
  ```

#### Checklist — Graph 1:
- [ ] Create `projects.csv` and `assignments.csv`
- [ ] Design schema (nodes, relationships, constraints, indexes)
- [ ] Ingest data into Neo4j
- [ ] Run `SHOW CONSTRAINTS` and `SHOW INDEXES` to verify
- [ ] Write and run 3–5 sample queries
- [ ] Note any modeling decisions you made and why

---

### Day 5–6: Build Domain Graph 2 — E-commerce (Product–Order–User)

#### Step 1: Create the dataset

Create these small CSVs (put in `phase3/data/`):

**`users.csv`** (10 users):
```csv
user_id,name,email,city
U001,Alice Johnson,alice@example.com,Mumbai
U002,Bob Smith,bob@example.com,Delhi
U003,Carol Williams,carol@example.com,Bangalore
U004,Dave Brown,dave@example.com,Chennai
U005,Eve Davis,eve@example.com,Pune
U006,Frank Wilson,frank@example.com,Hyderabad
U007,Grace Lee,grace@example.com,Mumbai
U008,Hank Taylor,hank@example.com,Delhi
U009,Ivy Anderson,ivy@example.com,Bangalore
U010,Jack Thomas,jack@example.com,Chennai
```

**`products.csv`** (15–20 products):
```csv
product_id,name,price,category
PRD001,Wireless Mouse,799,Electronics
PRD002,Mechanical Keyboard,2499,Electronics
PRD003,USB-C Hub,1299,Electronics
PRD004,Notebook Set,349,Stationery
PRD005,Ballpoint Pen Pack,199,Stationery
PRD006,Desk Lamp,1599,Home Office
PRD007,Monitor Stand,2999,Home Office
PRD008,Webcam HD,3499,Electronics
PRD009,Headphones,4999,Electronics
PRD010,Coffee Mug,499,Lifestyle
PRD011,Water Bottle,699,Lifestyle
PRD012,Laptop Bag,1899,Accessories
PRD013,Mouse Pad XL,599,Accessories
PRD014,Screen Cleaner,249,Accessories
PRD015,Standing Desk Mat,1999,Home Office
```

**`orders.csv`** (30–40 orders with line items):
```csv
order_id,user_id,product_id,quantity,unit_price,created_at,status
ORD001,U001,PRD001,1,799,2024-01-15,delivered
ORD001,U001,PRD004,2,349,2024-01-15,delivered
ORD002,U002,PRD002,1,2499,2024-01-20,delivered
ORD002,U002,PRD013,1,599,2024-01-20,delivered
ORD003,U003,PRD009,1,4999,2024-02-01,delivered
ORD004,U001,PRD006,1,1599,2024-02-10,delivered
ORD004,U001,PRD007,1,2999,2024-02-10,delivered
ORD005,U004,PRD008,1,3499,2024-02-15,shipped
ORD006,U005,PRD010,3,499,2024-02-20,delivered
ORD006,U005,PRD011,2,699,2024-02-20,delivered
ORD007,U002,PRD001,1,799,2024-03-01,delivered
ORD008,U006,PRD012,1,1899,2024-03-05,cancelled
ORD009,U003,PRD002,1,2499,2024-03-10,delivered
ORD009,U003,PRD003,1,1299,2024-03-10,delivered
ORD010,U007,PRD015,1,1999,2024-03-15,processing
```

#### Step 2: Design the schema

**Nodes:**
- `User` — `{user_id, name, email, city}`
- `Product` — `{product_id, name, price, category}`
- `Order` — `{order_id, created_at, status}`
- `Category` — `{name}` (optional: extract category to its own node to avoid filtering on string property)

**Relationships:**
- `(User)-[:PLACED]->(Order)`
- `(Order)-[:CONTAINS {quantity, unit_price}]->(Product)` — line items as relationship properties
- `(Product)-[:IN_CATEGORY]->(Category)` (optional — or keep category as a Product property)

**Constraints:**
```cypher
CREATE CONSTRAINT user_id IF NOT EXISTS FOR (u:User) REQUIRE u.user_id IS UNIQUE
CREATE CONSTRAINT product_id IF NOT EXISTS FOR (p:Product) REQUIRE p.product_id IS UNIQUE
CREATE CONSTRAINT order_id IF NOT EXISTS FOR (o:Order) REQUIRE o.order_id IS UNIQUE
```

**Indexes:**
```cypher
CREATE INDEX order_created IF NOT EXISTS FOR (o:Order) ON (o.created_at)
CREATE INDEX order_status IF NOT EXISTS FOR (o:Order) ON (o.status)
CREATE INDEX product_category IF NOT EXISTS FOR (p:Product) ON (p.category)
CREATE INDEX user_city IF NOT EXISTS FOR (u:User) ON (u.city)
```

#### Step 3: Ingest and verify

Write ingest script or use Neo4j Browser. Sample Cypher for one order line:
```cypher
MERGE (u:User {user_id: "U001"})
SET u.name = "Alice Johnson", u.email = "alice@example.com", u.city = "Mumbai"

MERGE (p:Product {product_id: "PRD001"})
SET p.name = "Wireless Mouse", p.price = 799, p.category = "Electronics"

MERGE (o:Order {order_id: "ORD001"})
SET o.created_at = date("2024-01-15"), o.status = "delivered"

MERGE (u)-[:PLACED]->(o)
MERGE (o)-[:CONTAINS {quantity: 1, unit_price: 799}]->(p)
```

#### Step 4: Sample queries

```cypher
// Total spend per user
MATCH (u:User)-[:PLACED]->(o:Order)-[c:CONTAINS]->(p:Product)
WHERE o.status = "delivered"
RETURN u.name, sum(c.quantity * c.unit_price) AS total_spend
ORDER BY total_spend DESC

// Most ordered products
MATCH (o:Order)-[c:CONTAINS]->(p:Product)
RETURN p.name, sum(c.quantity) AS total_ordered
ORDER BY total_ordered DESC LIMIT 5

// Users who bought Electronics
MATCH (u:User)-[:PLACED]->(o:Order)-[:CONTAINS]->(p:Product)
WHERE p.category = "Electronics"
RETURN DISTINCT u.name, collect(DISTINCT p.name) AS products

// Orders with more than 1 line item
MATCH (o:Order)-[c:CONTAINS]->()
WITH o, count(c) AS items
WHERE items > 1
RETURN o.order_id, items ORDER BY items DESC
```

#### Checklist — Graph 2:
- [ ] Create `users.csv`, `products.csv`, `orders.csv`
- [ ] Design schema (nodes, relationships, constraints, indexes)
- [ ] Ingest data into Neo4j (separate database or clear graph first)
- [ ] Run `SHOW CONSTRAINTS` and `SHOW INDEXES` to verify
- [ ] Write and run 4–6 sample queries
- [ ] Note modeling decisions: did you use a `Category` node or keep it as a property? Why?

---

## Week 2: Query Optimization & Profiling (Section 3.2)

### Day 7–8: Learn EXPLAIN and PROFILE

#### What is EXPLAIN?

Shows the **planned** execution without running the query. No actual data access. Use it to quickly see:
- Which operators the planner chose
- Whether indexes will be used
- The expected order of operations

```cypher
EXPLAIN MATCH (m:Movie)-[:HAS_GENRE]->(g:Genre {name: "Action"}) RETURN m.name
```

#### What is PROFILE?

**Runs** the query AND shows the execution plan with **actual metrics**:
- `Rows` — actual number of rows each operator processed
- `DbHits` — number of database operations (lower is better)
- `Time` — time spent at each operator

```cypher
PROFILE MATCH (m:Movie)-[:HAS_GENRE]->(g:Genre {name: "Action"}) RETURN m.name
```

#### How to read the plan

Plans are a tree of operators. Read from **bottom to top**:

| Operator | What it means | Good or bad? |
|----------|--------------|-------------|
| `NodeIndexSeek` | Uses an index to find nodes | Good |
| `NodeUniqueIndexSeek` | Uses a unique index | Good |
| `NodeByLabelScan` | Scans ALL nodes with that label | Bad if many nodes |
| `AllNodesScan` | Scans EVERY node in the database | Very bad |
| `Filter` | Filters rows after fetching | Fine, but wasteful if late |
| `Expand(All)` | Follows relationships | Normal; watch for high row counts |
| `EagerAggregation` | Aggregation (COUNT, SUM, etc.) | Normal |

**Key metrics to watch:**
- If a `NodeByLabelScan` has 2200 rows and you only need 10, you need an index.
- If `Expand` multiplies rows from 100 to 50,000, you have a potential supernode or missing filter.
- High `DbHits` on one operator = that's your bottleneck.

**References:**
- [Neo4j — Planning and tuning](https://neo4j.com/docs/cypher-manual/current/planning-and-tuning/)
- [Neo4j — Execution plans](https://neo4j.com/docs/cypher-manual/current/planning-and-tuning/execution-plans/)
- [Neo4j Support — EXPLAIN and PROFILE](https://support.neo4j.com/s/article/6638160188691-How-to-get-Cypher-query-execution-plans-using-EXPLAIN-and-PROFILE)

#### Exercise:
- [ ] Run `EXPLAIN` on any simple query. Read the plan top-to-bottom.
- [ ] Run `PROFILE` on the same query. Note the Rows and DbHits for each operator.

---

### Day 9–10: Profile Phase 1 Queries

Go to your Phase 1 movie graph and run EXPLAIN/PROFILE on these queries (or similar ones you wrote):

#### Query 1: Movies by genre
```cypher
PROFILE MATCH (m:Movie)-[:HAS_GENRE]->(g:Genre {name: "Action"})
RETURN m.name, m.year
ORDER BY m.year DESC
```
**Look for:** Is there an index on `Genre.name`? Do you see `NodeIndexSeek` or `NodeByLabelScan`?

#### Query 2: Movies by a specific director
```cypher
PROFILE MATCH (p:Person {name: "Atlee"})-[:DIRECTED]->(m:Movie)
RETURN m.name, m.year
```
**Look for:** Index on `Person.name`? How many DbHits?

#### Query 3: Co-actors (actors who acted in the same movie)
```cypher
PROFILE MATCH (p1:Person)-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(p2:Person)
WHERE p1.name < p2.name
RETURN p1.name, p2.name, m.name
LIMIT 20
```
**Look for:** This is a pattern match with two traversals. Watch the Expand operator — how many rows does it produce before the WHERE filter?

#### Query 4: Count movies per genre
```cypher
PROFILE MATCH (m:Movie)-[:HAS_GENRE]->(g:Genre)
RETURN g.name, count(m) AS movie_count
ORDER BY movie_count DESC
```
**Look for:** How many rows flow through the Expand? Is EagerAggregation efficient?

#### Query 5: Actors in more than N movies
```cypher
PROFILE MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
WITH p, count(m) AS movie_count
WHERE movie_count > 5
RETURN p.name, movie_count
ORDER BY movie_count DESC
```
**Look for:** How many Person nodes are scanned? Could an early filter help?

#### For each query, note:

| Query | Starting operator | Index used? | Total DbHits | Total Rows | Bottleneck operator | Possible improvement |
|-------|------------------|-------------|--------------|------------|--------------------|--------------------|
| 1 | ? | ? | ? | ? | ? | ? |
| 2 | ? | ? | ? | ? | ? | ? |
| 3 | ? | ? | ? | ? | ? | ? |
| 4 | ? | ? | ? | ? | ? | ? |
| 5 | ? | ? | ? | ? | ? | ? |

---

### Day 11–12: Apply and Document Optimizations

For 2–3 of the queries above, apply a concrete optimization and document in `OPTIMIZATIONS.md`.

#### Common optimizations to try

**1. Add an index:**
```cypher
CREATE INDEX genre_name IF NOT EXISTS FOR (g:Genre) ON (g.name)
CREATE INDEX person_name IF NOT EXISTS FOR (p:Person) ON (p.name)
CREATE INDEX movie_year IF NOT EXISTS FOR (m:Movie) ON (m.year)
```
Then re-run PROFILE and compare DbHits.

**2. Rewrite query to filter earlier:**

Before (filter after expand):
```cypher
MATCH (p:Person)-[:ACTED_IN]->(m:Movie)-[:HAS_GENRE]->(g:Genre)
WHERE g.name = "Action" AND m.year > 2020
RETURN p.name, m.name
```

After (filter the most selective node first):
```cypher
MATCH (g:Genre {name: "Action"})<-[:HAS_GENRE]-(m:Movie)
WHERE m.year > 2020
MATCH (p:Person)-[:ACTED_IN]->(m)
RETURN p.name, m.name
```

**3. Add LIMIT to prevent unnecessary traversals:**
```cypher
MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
RETURN p.name, m.name
LIMIT 25
```

**4. Use WITH to control cardinality:**
```cypher
MATCH (g:Genre {name: "Action"})<-[:HAS_GENRE]-(m:Movie)
WITH m
MATCH (p:Person)-[:ACTED_IN]->(m)
RETURN p.name, m.name
```

#### Document each optimization in `OPTIMIZATIONS.md`

For each optimization, fill in:
- **Query:** The Cypher query (before optimization).
- **Before:** What PROFILE showed (operator, DbHits, rows).
- **Change:** What you did (added index, rewrote query, added LIMIT).
- **After:** What PROFILE showed after the change.

---

### Day 13–14: Review and Clean Up

- [ ] Review all five EXPLAIN/PROFILE notes. Make sure they are clear.
- [ ] Verify `OPTIMIZATIONS.md` has 2–3 complete entries.
- [ ] Run `SHOW INDEXES` on all your databases (movie, employee, e-commerce) — are indexes in place?
- [ ] Run `SHOW CONSTRAINTS` — are uniqueness constraints covering all key properties?
- [ ] Write a short summary (3–5 sentences) at the top of `OPTIMIZATIONS.md`: what you learned about query optimization.

---

## Checklist (Phase 3 at a glance)

### Week 1: Modeling

- [ ] **Topic 1:** Labels vs relationship types — read + exercise
- [ ] **Topic 2:** Property modeling — read + exercise
- [ ] **Topic 3:** Avoiding supernodes — read + degree query exercise
- [ ] **Topic 4:** Many-to-many and intermediate nodes — read + exercise
- [ ] **Topic 5:** Temporal modeling — read + Cypher exercise
- [ ] **Graph 1:** Employee–Project–Department
  - [ ] Create CSVs (projects.csv, assignments.csv)
  - [ ] Design schema
  - [ ] Ingest into Neo4j
  - [ ] Add constraints and indexes
  - [ ] Run 3–5 sample queries
- [ ] **Graph 2:** E-commerce Product–Order–User
  - [ ] Create CSVs (users.csv, products.csv, orders.csv)
  - [ ] Design schema
  - [ ] Ingest into Neo4j
  - [ ] Add constraints and indexes
  - [ ] Run 4–6 sample queries

### Week 2: Optimization

- [ ] **Learn:** EXPLAIN vs PROFILE (when, how, what to look for)
- [ ] **Learn:** Query plan operators, index usage, cardinality, bottlenecks
- [ ] **Profile:** Run EXPLAIN/PROFILE on 5 Phase 1 queries; fill in notes table
- [ ] **Optimize:** Apply 2–3 optimizations (index, rewrite, LIMIT)
- [ ] **Document:** Fill in `OPTIMIZATIONS.md` with before/change/after
- [ ] **Review:** Summary, verify all indexes and constraints

---

## References Summary

### Official Neo4j Documentation

| Topic | URL |
|-------|-----|
| Planning and tuning (EXPLAIN, PROFILE) | https://neo4j.com/docs/cypher-manual/current/planning-and-tuning/ |
| Execution plans | https://neo4j.com/docs/cypher-manual/current/planning-and-tuning/execution-plans/ |
| Create indexes | https://neo4j.com/docs/cypher-manual/current/indexes/search-performance-indexes/create-indexes/ |
| Constraints | https://neo4j.com/docs/cypher-manual/current/constraints/ |
| Temporal values (date, datetime) | https://neo4j.com/docs/cypher-manual/current/values-and-types/temporal/ |

### Articles and Blogs

| Topic | URL |
|-------|-----|
| Graph modeling: Labels | https://medium.com/neo4j/graph-modeling-labels-71775ff7d121 |
| Graph modeling: Super nodes | https://medium.com/neo4j/graph-modeling-all-about-super-nodes-d6ad7e11015b |
| Best practices: Data modeling | https://neo4j.guide/article/Best_Practices_for_Neo4j_Data_Modeling.html |
| Temporal versioning in Neo4j | https://dev.to/satyam_shree_087caef77512/a-practical-guide-to-temporal-versioning-in-neo4j-nodes-relationships-and-historical-graph-1m5g |
| Tuning Cypher queries | https://neo4j.com/blog/tuning-cypher-queries/ |
| Understanding Cypher cardinality | https://neo4j.com/developer/kb/understanding-cypher-cardinality/ |

### Free Courses (Neo4j Graph Academy)

| Course | Duration | URL |
|--------|----------|-----|
| Graph Data Modeling Fundamentals | ~2 hours | https://graphacademy.neo4j.com/courses/modeling-fundamentals/ |
| Cypher Fundamentals | ~1 hour | https://graphacademy.neo4j.com/courses/cypher-fundamentals/ |
| Intermediate Cypher Queries | ~4 hours | https://graphacademy.neo4j.com/courses/cypher-intermediate-queries |
| Cypher Patterns (advanced) | — | https://graphacademy.neo4j.com/courses/cypher-patterns/ |

---

**Next:** After Phase 3, proceed to Phase 4 — Graph Intelligence (GDS algorithms: PageRank, shortest path, community detection).
