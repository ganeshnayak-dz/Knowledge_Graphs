from neo4j import GraphDatabase
from core.config import settings


class Neo4jConnection:

    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password)
        )

    def close(self):
        self.driver.close()

    def execute(self, query: str, parameters: dict | None = None):
        with self.driver.session(database=settings.neo4j_db) as session:
            session.run(query, parameters or {})
    
    def execute_query(self, query: str, parameters: dict | None = None):
        with self.driver.session(database=settings.neo4j_db) as session:
            result = session.run(query, parameters or {})
            return list(result) 
