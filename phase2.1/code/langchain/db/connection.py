"""
Single place for all Neo4j connection logic (credentials from core.config).

- Ingest and direct Cypher: use get_neo4j_connection() or Neo4jConnection.
- LangChain chains (NL→Cypher): use get_graph() → Neo4jGraph.
"""
from typing import Optional

from langchain_neo4j import Neo4jGraph
from neo4j import GraphDatabase

from core.config import settings


class Neo4jConnection:
    """Raw Neo4j driver wrapper. Use for ingest (CSV → Cypher MERGE). Call .close() when done."""

    def __init__(self) -> None:
        self.driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password),
        )

    def close(self) -> None:
        self.driver.close()

    def execute(self, query: str, parameters: Optional[dict] = None) -> None:
        with self.driver.session(database=settings.neo4j_db) as session:
            session.run(query, parameters or {})

    def execute_query(self, query: str, parameters: Optional[dict] = None):
        with self.driver.session(database=settings.neo4j_db) as session:
            result = session.run(query, parameters or {})
            return list(result)


def get_neo4j_connection() -> Neo4jConnection:
    """Return a new Neo4j connection for ingest or direct Cypher. Caller must call .close()."""
    return Neo4jConnection()


# Cached LangChain graph for chains (GraphCypherQAChain).
_graph: Optional[Neo4jGraph] = None


def get_graph() -> Neo4jGraph:
    """Return a shared Neo4jGraph for LangChain chains (e.g. NL→Cypher). Same config as raw driver."""
    global _graph
    if _graph is None:
        _graph = Neo4jGraph(
            url=settings.neo4j_uri,
            username=settings.neo4j_user,
            password=settings.neo4j_password,
            database=settings.neo4j_db,
        )
    return _graph


def close_graph() -> None:
    """Close the cached LangChain graph (e.g. on shutdown)."""
    global _graph
    if _graph is not None:
        _graph.close()
        _graph = None
