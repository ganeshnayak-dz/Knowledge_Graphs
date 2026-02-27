"""Graph schema (labels, relationship types, constraints). Fill as you learn."""
CREATE_CONSTRAINS = [
    """
    CREATE CONSTRAINT movie_id IF NOT EXISTS
    FOR (m:Movie) REQUIRE m.movie_id IS UNIQUE
    """,
    """
    CREATE CONSTRAINT person_name IF NOT EXISTS
    FOR (p:Person) REQUIRE p.name IS UNIQUE
    """,
    """
    CREATE CONSTRAINT genre_name IF NOT EXISTS
    FOR (g:Genre) REQUIRE g.name IS UNIQUE
    """
]


# Queries
CREATE_MOVIE="""
MERGE (m:Movie {movie_id:$movie_id})
SET m.name=$movie_name,
m.year=$year,
m.overview=$overview
"""


CREATE_GENRE_REL = """
MERGE (g:Genre {name: $genre})
WITH g
MATCH (m:Movie {movie_id: $movie_id})
MERGE (m)-[:HAS_GENRE]->(g)
"""

CREATE_DIRECTOR_REL = """
MERGE (p:Person {name: $director})
WITH p
MATCH (m:Movie {movie_id: $movie_id})
MERGE (p)-[:DIRECTED]->(m)
"""

CREATE_ACTOR_REL = """
MERGE (p:Person {name: $actor})
WITH p
MATCH (m:Movie {movie_id: $movie_id})
MERGE (p)-[:ACTED_IN]->(m)
"""