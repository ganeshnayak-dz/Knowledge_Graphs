# Decision Guide: When to Use a Knowledge Graph, RAG, or Neither

**Status:** Draft — refine as you learn (especially after Phases 2, 7, and the small project).

**Purpose:** A flowchart-style guide to decide **when to use a Knowledge Graph**, **when to use RAG**, and **when not to use** either for your project.

---

## Flowchart (Mermaid)

```mermaid
flowchart TD
    START([What are you building?]) --> Q1{Do you need exact<br/>relationships & multi-hop<br/>reasoning?}
    Q1 -->|Yes| Q2{Do you also have<br/>documents or need<br/>semantic search?}
    Q1 -->|No| Q3{Do you mainly have<br/>unstructured documents<br/>or need semantic search?}
    
    Q2 -->|Yes| HYBRID[Consider Hybrid:<br/>Graph + Vector + LLM]
    Q2 -->|No| KG[Use Knowledge Graph]
    
    Q3 -->|Yes| Q4{Do you need quick<br/>prototype & no schema?}
    Q3 -->|No| Q5{Is it simple CRUD,<br/>flat data, or key-value?}
    
    Q4 -->|Yes| RAG[Use RAG<br/>Vector + LLM]
    Q4 -->|No| HYBRID
    
    Q5 -->|Yes| NEITHER[Neither KG nor RAG:<br/>Relational DB or<br/>simple storage may be enough]
    Q5 -->|No| Q1
    
    KG --> KG_NOTE[Good for: fraud, recommendations,<br/>enterprise integration, compliance]
    RAG --> RAG_NOTE[Good for: Q&A over docs,<br/>chatbot, semantic search]
    HYBRID --> HYBRID_NOTE[Good for: serious AI systems<br/>that need both structure & semantics]
    NEITHER --> NEITHER_NOTE[Good for: apps, config,<br/>simple reporting]
```

---

## Short narrative (by outcome)

| Outcome | When it fits |
|--------|----------------|
| **Knowledge Graph** | You need **exact relationships**, **multi-hop queries**, deterministic answers, or use cases like fraud detection, recommendations, enterprise data integration, or regulatory compliance. Data is (or can be) structured into entities and relationships. |
| **RAG** | You mainly have **unstructured documents** (PDFs, articles), need **semantic search** or Q&A over a knowledge base, want a **fast prototype**, and don’t need strict multi-hop logic. |
| **Hybrid (Graph + Vector + LLM)** | You need **both** relationship reasoning and semantic/document search — e.g. graph for facts and structure, vector for “similar to this” and document context, LLM to combine and answer. |
| **Neither** | Your problem is **simple CRUD**, flat or key-value data, or well-served by a **relational database**. Adding KG or RAG would be unnecessary complexity. |

---

## References

- [RAG vs Knowledge Graph](rag-vs-knowledge-graph.md) — detailed comparison
- [Hybrid Architecture](hybrid-architecture.md) — graph + vector + LLM flow
- [plan.md](../plan.md) — learning phases (e.g. Phase 7 = hybrid)

---

*Edit this file as you complete more phases and get a clearer sense of when each approach fits.*
