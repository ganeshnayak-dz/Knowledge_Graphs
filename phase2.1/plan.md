# Phase 2.1 — Plan: KG Creation with Frameworks

**Goal:** Use LangChain, LlamaIndex, and Haystack to build knowledge graphs from **both structured and unstructured data**. Compare how each framework handles graph construction, entity extraction, and NL→Cypher. This complements the custom pipeline you built in Phase 2.

**Duration:** ~3 weeks.

**Prerequisites:**
- Phase 1 and Phase 2 complete (movie graph + employee NL→Cypher pipeline running).
- Neo4j running locally.
- At least one LLM API key (Groq, OpenAI, or Anthropic).

---

## Why Both Structured AND Unstructured?

| Data type | What you learn | Prepares you for |
|-----------|---------------|------------------|
| **Structured** (CSV) | How each framework ingests tabular data into Neo4j, creates nodes/relationships, and exposes NL→Cypher | Comparing frameworks fairly against your Phase 2 custom code |
| **Unstructured** (text) | How each framework uses LLMs to **extract entities and relationships** from free text | Phase 6 (LLM extraction), Phase 7 (hybrid RAG), Phase 9 (capstone) |

Doing only structured would miss the most powerful feature of these frameworks: automated entity extraction from text.

---

## Data Sources

### Structured data (reuse what you have)
- `phase1/data/movie.csv` — movie metadata (2200 rows): movie_id, name, year, genre, overview, director, cast.
- `phase2/data/employee.csv` — employee data (200 rows): name, age, department, position, salary, etc.

Pick **one** CSV per framework (movie.csv is recommended — it has richer relationships).

### Unstructured data (new — small scale)
- **Option A:** Use the `overview` column from `movie.csv` — each row already has a plot summary paragraph. Extract entities (characters, themes, locations) from these summaries.
- **Option B:** Collect 10–15 short Wikipedia paragraphs about movies or actors (copy-paste into a `texts/` folder or a simple JSON file).
- **Option C:** Use 5–10 news article snippets on any domain you find interesting.

**Recommendation:** Start with Option A (movie overviews) since the data is already in your repo.

---

## Order of Work

| Step | What | Framework | Data | Duration |
|------|------|-----------|------|----------|
| 1 | Structured KG + NL→Cypher | LangChain | movie.csv | 3–4 days |
| 2 | Unstructured text → KG | LangChain | movie overviews | 2–3 days |
| 3 | Structured KG + NL→Cypher | LlamaIndex | movie.csv | 3–4 days |
| 4 | Unstructured text → KG | LlamaIndex | movie overviews | 2–3 days |
| 5 | Structured KG + NL→Cypher | Haystack | movie.csv | 2–3 days |
| 6 | Unstructured text → KG | Haystack | movie overviews | 2–3 days |
| 7 | Write comparison notes | All | — | 1 day |

Start with LangChain — it has the most mature KG tooling and will be easiest to get working first.

---

## Framework 1: LangChain

### Packages to install

Add these to `code/langchain/requirements.txt`:

```
langchain
langchain-community
langchain-experimental
langchain-neo4j
langchain-groq            # or langchain-openai / langchain-anthropic
neo4j
python-dotenv
```

### Key classes you will use

| Class | Package | What it does |
|-------|---------|-------------|
| `Neo4jGraph` | `langchain_neo4j` | Connects to Neo4j; auto-generates schema via `refresh_schema()` |
| `GraphCypherQAChain` | `langchain_neo4j` | NL question → Cypher → execute → LLM formats answer |
| `LLMGraphTransformer` | `langchain_experimental.graph_transformers` | Text → extracted entities and relationships (graph documents) |
| `ChatGroq` / `ChatOpenAI` | `langchain_groq` / `langchain_openai` | LLM provider |

### Task A: Structured data → KG + NL→Cypher

**Files to fill:**

1. **`core/config.py`** — Load `.env` (Neo4j URI, credentials, API keys, LLM provider choice).

2. **`graph/connection.py`** — Create a `Neo4jGraph` instance:
   ```python
   from langchain_neo4j import Neo4jGraph

   graph = Neo4jGraph(
       url="neo4j://localhost:7687",
       username="neo4j",
       password="your_password",
       database="movies"  # or your DB name
   )
   ```

3. **`graph/schema.py`** — Define Cypher statements for constraints and MERGE queries (similar to Phase 1's `graph/schema.py`). Or use `graph.refresh_schema()` to auto-detect.

4. **`ingest/load_data.py`** — Load `movie.csv`, iterate rows, execute Cypher MERGEs via `graph.query(cypher, params)`:
   ```python
   graph.query(
       "MERGE (m:Movie {movie_id: $movie_id}) SET m.name = $name, m.year = $year",
       {"movie_id": row["movie_id"], "name": row["movie_name"], "year": row["year"]}
   )
   ```

5. **`graph/builder.py`** — Build the `GraphCypherQAChain` for NL→Cypher:
   ```python
   from langchain_neo4j import GraphCypherQAChain

   chain = GraphCypherQAChain.from_llm(
       llm=your_llm,
       graph=graph,
       verbose=True,
       validate_cypher=True,
       allow_dangerous_requests=True
   )
   result = chain.invoke({"query": "Which actors appeared in Jawan?"})
   ```

6. **`llm/providers/groq.py`** (or openai.py) — Initialize the LLM:
   ```python
   from langchain_groq import ChatGroq

   llm = ChatGroq(model="llama-3.1-70b-versatile", api_key="...")
   ```

**Checklist — Structured (LangChain):**
- [ ] Install packages; verify imports work
- [ ] `core/config.py` loads `.env` with Neo4j + LLM settings
- [ ] `graph/connection.py` creates `Neo4jGraph` and connects
- [ ] `graph/schema.py` defines constraints (reuse Phase 1 Cypher)
- [ ] `ingest/load_data.py` loads movie.csv into Neo4j
- [ ] `graph/builder.py` builds `GraphCypherQAChain`
- [ ] Test: ask 3–5 natural language questions, verify Cypher + results
- [ ] Compare: how does `GraphCypherQAChain` differ from your Phase 2 custom pipeline?

### Task B: Unstructured text → KG

**What to do:**

1. Prepare text data — extract `overview` from movie.csv (or load separate text files).
2. Convert to LangChain `Document` objects.
3. Use `LLMGraphTransformer` to extract entities and relationships:
   ```python
   from langchain_experimental.graph_transformers import LLMGraphTransformer
   from langchain_core.documents import Document

   transformer = LLMGraphTransformer(llm=your_llm)

   documents = [Document(page_content=overview_text)]
   graph_documents = transformer.convert_to_graph_documents(documents)
   ```
4. Inspect extracted nodes and relationships in `graph_documents`.
5. Store in Neo4j:
   ```python
   graph.add_graph_documents(graph_documents)
   ```
6. Query the newly created graph to see what was extracted.

**Optional — constrain extraction:**
- Pass `allowed_nodes` and `allowed_relationships` to `LLMGraphTransformer` so it only extracts entity types you care about (e.g. `["Person", "Movie", "Location"]`).

**Checklist — Unstructured (LangChain):**
- [ ] Prepare 10–20 text snippets (movie overviews or other)
- [ ] Convert to `Document` objects
- [ ] Run `LLMGraphTransformer` and inspect extracted graph documents
- [ ] Store extracted graph in Neo4j (use a separate database or clear first)
- [ ] Query Neo4j to verify extracted nodes and relationships
- [ ] Optional: use `allowed_nodes` / `allowed_relationships` to constrain extraction
- [ ] Note: quality of extraction, types of entities found, any hallucinations

---

## Framework 2: LlamaIndex

### Packages to install

Add these to `code/llamaindex/requirements.txt`:

```
llama-index
llama-index-graph-stores-neo4j
llama-index-llms-groq        # or llama-index-llms-openai
llama-index-embeddings-openai # or another embedding provider
neo4j
python-dotenv
```

### Key classes you will use

| Class | Package | What it does |
|-------|---------|-------------|
| `Neo4jPropertyGraphStore` | `llama_index.graph_stores.neo4j` | Neo4j as property graph backend |
| `PropertyGraphIndex` | `llama_index.core` | Builds a KG index from documents; supports querying |
| `SchemaLLMPathExtractor` | `llama_index.core.indices.property_graph` | LLM extracts (entity)→[relation]→(entity) triples constrained by a schema |
| `ImplicitPathExtractor` | `llama_index.core.indices.property_graph` | Rule-based extraction (keywords, noun chunks) |
| `Groq` / `OpenAI` | `llama_index.llms.groq` / `llama_index.llms.openai` | LLM provider |

### Task A: Structured data → KG

**Files to fill:**

1. **`core/config.py`** — Load `.env`; set up `Settings` (LlamaIndex global settings for LLM and embedding model).

2. **`graph/connection.py`** — Create `Neo4jPropertyGraphStore`:
   ```python
   from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore

   graph_store = Neo4jPropertyGraphStore(
       username="neo4j",
       password="your_password",
       url="bolt://localhost:7687",
       database="movies"
   )
   ```

3. **`ingest/load_data.py`** — Load movie.csv; convert each row into a LlamaIndex `Document`:
   ```python
   from llama_index.core import Document

   documents = []
   for row in csv_data:
       text = f"Movie: {row['movie_name']} ({row['year']}). Genre: {row['genre']}. Director: {row['director']}. Cast: {row['cast']}."
       documents.append(Document(text=text, metadata={"movie_id": row["movie_id"]}))
   ```

4. **`graph/builder.py`** — Build `PropertyGraphIndex`:
   ```python
   from llama_index.core import PropertyGraphIndex

   index = PropertyGraphIndex.from_documents(
       documents,
       property_graph_store=graph_store,
       llm=your_llm,
       show_progress=True,
   )
   ```

5. **Query the graph:**
   ```python
   query_engine = index.as_query_engine(include_text=True)
   response = query_engine.query("Which actors appeared in Jawan?")
   ```

**Checklist — Structured (LlamaIndex):**
- [ ] Install packages; verify imports
- [ ] `core/config.py` loads settings and configures LlamaIndex `Settings`
- [ ] `graph/connection.py` creates `Neo4jPropertyGraphStore`
- [ ] `ingest/load_data.py` converts CSV rows to `Document` objects
- [ ] `graph/builder.py` builds `PropertyGraphIndex` from documents
- [ ] Test: query the index with 3–5 questions
- [ ] Compare: how does the graph structure differ from Phase 1's manual Cypher approach?

### Task B: Unstructured text → KG

**What to do:**

1. Prepare text documents (movie overviews or other text).
2. Use `SchemaLLMPathExtractor` with allowed entity/relation types:
   ```python
   from llama_index.core.indices.property_graph import SchemaLLMPathExtractor

   kg_extractor = SchemaLLMPathExtractor(
       llm=your_llm,
       possible_entities=["Person", "Movie", "Genre", "Location", "Character"],
       possible_relations=["ACTED_IN", "DIRECTED", "SET_IN", "ABOUT", "FEATURES"],
   )
   ```
3. Build the index with the extractor:
   ```python
   index = PropertyGraphIndex.from_documents(
       documents,
       property_graph_store=graph_store,
       kg_extractors=[kg_extractor],
       llm=your_llm,
       show_progress=True,
   )
   ```
4. Also try `ImplicitPathExtractor` (no LLM needed — rule-based) and compare quality.
5. Query and inspect what was extracted.

**Checklist — Unstructured (LlamaIndex):**
- [ ] Prepare text documents (movie overviews)
- [ ] Configure `SchemaLLMPathExtractor` with entity and relation types
- [ ] Build `PropertyGraphIndex` with the extractor
- [ ] Query the index; inspect extracted triples in Neo4j
- [ ] Try `ImplicitPathExtractor` and compare extraction quality
- [ ] Note: differences vs LangChain's `LLMGraphTransformer`

---

## Framework 3: Haystack

### Packages to install

Add these to `code/haystack/requirements.txt`:

```
haystack-ai
neo4j-haystack
neo4j
python-dotenv
```

### Key classes you will use

| Class | Package | What it does |
|-------|---------|-------------|
| `Neo4jDocumentStore` | `neo4j_haystack` | Store and retrieve documents in Neo4j |
| `Pipeline` | `haystack` | Build composable pipelines (ingest, query, etc.) |
| `ChatPromptBuilder` | `haystack.components.builders` | Build prompts for LLM |
| `OpenAIGenerator` / `GroqGenerator` | `haystack.components.generators` | LLM provider |

### Important note about Haystack

Haystack is strongest for **document pipelines and RAG**. Its native KG construction support is **less mature** than LangChain or LlamaIndex. You will likely need to:
- Use the Neo4j Python driver directly for graph construction (Cypher MERGEs)
- Build custom Haystack pipeline components for entity extraction → graph storage
- Use `neo4j-haystack` mainly for document storage and retrieval

This is a valuable learning: **not every framework is equally strong for KG construction**. Document this finding — it feeds directly into your decision guide.

### Task A: Structured data → KG

**Files to fill:**

1. **`core/config.py`** — Load `.env` with Neo4j and LLM settings.

2. **`graph/connection.py`** — Create Neo4j connection (direct driver or `Neo4jDocumentStore`):
   ```python
   from neo4j import GraphDatabase

   driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "password"))
   ```

3. **`graph/schema.py`** — Same constraints as Phase 1 (Cypher statements).

4. **`ingest/load_data.py`** — Build a Haystack pipeline to load CSV:
   ```python
   from haystack import Pipeline
   # Read CSV -> transform rows -> execute Cypher via Neo4j driver
   ```
   Since Haystack doesn't have a built-in CSV→Graph component, you'll parse the CSV yourself and execute Cypher through the driver (similar to Phase 1 but wrapped in a Haystack pipeline structure).

5. **`graph/builder.py`** — Build a query pipeline:
   - Use `ChatPromptBuilder` to create a prompt with schema + question
   - Use a generator (LLM) to produce Cypher
   - Execute via Neo4j driver
   - This is essentially building your Phase 2 NL→Cypher pipeline using Haystack components

**Checklist — Structured (Haystack):**
- [ ] Install packages; verify imports
- [ ] `core/config.py` loads settings
- [ ] `graph/connection.py` connects to Neo4j
- [ ] `ingest/load_data.py` ingests movie.csv (via pipeline or direct)
- [ ] `graph/builder.py` builds a query pipeline (NL → Cypher → results)
- [ ] Test: ask 3–5 questions
- [ ] Note: how much was "Haystack" vs "custom code using Neo4j driver"?

### Task B: Unstructured text → KG

**What to do:**

1. Build a custom Haystack component for entity extraction:
   ```python
   from haystack import component

   @component
   class EntityExtractor:
       """Use LLM to extract entities and relationships from text."""

       @component.output_types(entities=list, relationships=list)
       def run(self, text: str):
           # Prompt LLM to extract entities/relationships
           # Parse structured output
           # Return entities and relationships
           ...
   ```
2. Build a pipeline: `DocumentReader → EntityExtractor → Neo4jWriter`.
3. The Neo4j writer component executes MERGE Cypher to store extracted entities.
4. Compare: how much more manual work is this vs LangChain/LlamaIndex?

**Checklist — Unstructured (Haystack):**
- [ ] Create a custom `EntityExtractor` component
- [ ] Create a custom `Neo4jGraphWriter` component
- [ ] Build a pipeline connecting them
- [ ] Run on movie overviews; inspect results in Neo4j
- [ ] Note: significantly more manual work than LangChain/LlamaIndex — document this

---

## Deliverable: Framework Comparison

After completing all three frameworks, fill in this comparison table (create as `phase2.1/COMPARISON.md` or add to this file):

### Comparison Table

| Aspect | LangChain | LlamaIndex | Haystack |
|--------|-----------|------------|----------|
| **Structured CSV → KG** | | | |
| Ease of setup | ? / 5 | ? / 5 | ? / 5 |
| Lines of code needed | ~? | ~? | ~? |
| Built-in Neo4j support | `Neo4jGraph` | `Neo4jPropertyGraphStore` | `neo4j-haystack` (community) |
| **Unstructured text → KG** | | | |
| Built-in extractor | `LLMGraphTransformer` | `SchemaLLMPathExtractor` | Custom component needed |
| Schema constraints | `allowed_nodes` / `allowed_relationships` | `possible_entities` / `possible_relations` | Manual |
| Extraction quality | ? / 5 | ? / 5 | ? / 5 |
| **NL → Cypher** | | | |
| Built-in chain | `GraphCypherQAChain` | `KnowledgeGraphQueryEngine` | Custom pipeline |
| Answer quality | ? / 5 | ? / 5 | ? / 5 |
| **Overall** | | | |
| Best for | ? | ? | ? |
| Weakest at | ? | ? | ? |
| When to choose | ? | ? | ? |

### Questions to answer in your comparison

1. Which framework required the least code to go from CSV → working KG?
2. Which framework produced the best entity extraction from unstructured text?
3. Which framework's NL→Cypher was most accurate compared to your Phase 2 custom pipeline?
4. For which use case would you pick each framework?
5. What could each framework NOT do (or did poorly)?

---

## References

### LangChain

| Resource | URL |
|----------|-----|
| LangChain Neo4j integration | https://python.langchain.com/docs/integrations/graphs/neo4j/ |
| GraphCypherQAChain | https://python.langchain.com/docs/how_to/graph_cypher_qa/ |
| LLMGraphTransformer | https://python.langchain.com/docs/how_to/graph_constructing/ |
| LangChain Graph use cases | https://python.langchain.com/docs/tutorials/graph/ |

### LlamaIndex

| Resource | URL |
|----------|-----|
| Property Graph Index | https://docs.llamaindex.ai/en/stable/module_guides/indexing/property_graph_index/ |
| Neo4j Graph Store | https://docs.llamaindex.ai/en/stable/examples/property_graph/property_graph_neo4j/ |
| KG Extractors (Schema, Implicit) | https://docs.llamaindex.ai/en/stable/module_guides/indexing/property_graph_index/#kg-extractors |

### Haystack

| Resource | URL |
|----------|-----|
| Haystack Documentation | https://docs.haystack.deepset.ai/docs/intro |
| neo4j-haystack integration | https://haystack.deepset.ai/integrations/neo4j-document-store |
| Custom Components | https://docs.haystack.deepset.ai/docs/custom-components |

---

## Checklist (Phase 2.1 at a glance)

**LangChain**
- [ ] Structured: CSV → Neo4j KG via `Neo4jGraph` + Cypher
- [ ] Structured: NL→Cypher via `GraphCypherQAChain`
- [ ] Unstructured: Text → entities via `LLMGraphTransformer`
- [ ] Unstructured: Store extracted graph in Neo4j

**LlamaIndex**
- [ ] Structured: CSV → `Document` objects → `PropertyGraphIndex`
- [ ] Structured: Query via `query_engine`
- [ ] Unstructured: Text → entities via `SchemaLLMPathExtractor`
- [ ] Unstructured: Compare with `ImplicitPathExtractor`

**Haystack**
- [ ] Structured: CSV → Neo4j KG via pipeline + driver
- [ ] Structured: NL→Cypher via custom pipeline
- [ ] Unstructured: Custom `EntityExtractor` component
- [ ] Unstructured: Pipeline → Neo4j

**Comparison**
- [ ] Fill in comparison table
- [ ] Answer the 5 comparison questions
- [ ] Note findings for the decision guide (proposal deliverable)

---

**Next:** After Phase 2.1, proceed to Phase 3 (Graph Engineering) to strengthen your graph modeling and query optimization skills.
