"""NL→Cypher via LangChain GraphCypherQAChain — use the Neo4j-specific chain with Neo4jGraph."""
from langchain_neo4j import GraphCypherQAChain

from db.connection import get_graph
from llm import get_llm_for_chain


def get_qa_chain(verbose: bool = True) -> GraphCypherQAChain:
    """Build GraphCypherQAChain from configured LLM and Neo4j graph (direct LangChain usage)."""
    llm = get_llm_for_chain()
    graph = get_graph()
    return GraphCypherQAChain.from_llm(
        llm=llm,
        graph=graph,
        allow_dangerous_requests=True,
        verbose=verbose,
    )


def ask_graph(question: str, verbose: bool = True) -> dict:
    """Invoke the chain with the question; returns the raw chain response (e.g. response['result'])."""
    chain = get_qa_chain(verbose=verbose)
    return chain.invoke({"query": question})