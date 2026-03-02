# Notes — Learning Reference

This folder contains **concept notes** to support the [Knowledge Graph learning plan](../plan.md). Use them to clarify ideas, compare approaches, and share the repo as a learning resource.

---

## Index

| Note | What it covers |
|------|----------------|
| [Decision Guide (flowchart)](decision-guide.md) | **When to use KG vs RAG vs neither** — flowchart (Mermaid) + short narrative. Draft; refine as you learn. |
| [RAG vs Knowledge Graph](rag-vs-knowledge-graph.md) | RAG and Knowledge Graphs are not competitors. When to use each, pros/cons, and why hybrid systems use both. |
| [Hybrid Architecture](hybrid-architecture.md) | Graph + vector + LLM flow; how it fits the repo’s phases (including RAG and agents). |
| [LangChain: framework vs custom](langchain-framework-and-usage.md) | What “using the LangChain framework” means; chain (e.g. GraphCypherQAChain) vs custom pipeline; where things go in phase2.1. |
| [Ingestion: manual vs LLM](ingestion-manual-vs-llm.md) | When ingestion is manual (structured data) vs LLM-based (unstructured text); when to use which. |
| [Phase 2.1 tips](phase2.1-tips.md) | **What I learnt:** one connection module (two entry points), when to use raw vs graph, framework vs custom, folder layout. |
| [Glossary](glossary.md) | Short definitions for terms used in the plan and codebase. |

---

## How to Use This Repo to Learn

1. **Start with the plan** — [plan.md](../plan.md) is the roadmap (Phases 1–9). Follow phases in order when possible.
2. **Phase 1** — Pure graph: ingest, Cypher, constraints. No LLM. See [phase1/](../phase1/) and [phase2/code/](../phase2/code/) for structure.
3. **Phase 2** — NL→Cypher: ask in English, validate, run on graph. See `nl2cypher/`, `ask.py`, and optional `ask_langchain.py`.
4. **Read the notes** when you hit a concept (e.g. “What’s the difference between RAG and a knowledge graph?” → [rag-vs-knowledge-graph.md](rag-vs-knowledge-graph.md); “What does using the LangChain framework mean?” → [langchain-framework-and-usage.md](langchain-framework-and-usage.md); “Manual vs LLM ingestion?” → [ingestion-manual-vs-llm.md](ingestion-manual-vs-llm.md)).
5. **Later phases** — Graph engineering, algorithms (GDS), KG design, LLM extraction, hybrid RAG, agents, capstone. All are outlined in [plan.md](../plan.md).

---

## For Others Using This Repo

- **Goal of the repo:** Learn knowledge graph creation end-to-end: graph foundation → NL→Cypher → algorithms → KG design → extraction → hybrid (RAG) → agents → one capstone project.
- **Notes** = concept reference only; they don’t replace running the code and doing the plan.
- **Code** = Phase 1 (phase1/) and Phase 2 (phase2/code/) with optional LangChain path. Later phases are described in the plan; implement them in your own branch or fork.

If you want to “master it”: follow the plan phase by phase, run and modify the code, and use these notes to solidify the ideas (RAG vs KG, hybrid, glossary).
