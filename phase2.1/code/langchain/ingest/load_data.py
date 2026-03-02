"""Load and parse movie CSV and write to Neo4j (manual ingestion). Uses db.connection + graph.schema."""
import pandas as pd

from db.connection import get_neo4j_connection
from graph import schema
from models.movie import MovieModel


def ingest_movies(file_path: str) -> None:
    """Load movie CSV, apply schema constraints, and create Movie/Genre/Person nodes and relationships."""
    df = pd.read_csv(file_path)
    db = get_neo4j_connection()
    try:
        for constraint in schema.CREATE_CONSTRAINTS:
            db.execute(constraint)

        for _, row in df.iterrows():
            try:
                movie = MovieModel(**row.to_dict())
            except Exception as e:
                print(f"Validation failed: {e}")
                continue

            db.execute(schema.CREATE_MOVIE, movie.model_dump())

            for genre in movie.genre:
                db.execute(
                    schema.CREATE_GENRE_REL,
                    {"movie_id": movie.movie_id, "genre": genre},
                )

            db.execute(
                schema.CREATE_DIRECTOR_REL,
                {"movie_id": movie.movie_id, "director": movie.director},
            )

            for actor in movie.cast:
                db.execute(
                    schema.CREATE_ACTOR_REL,
                    {"movie_id": movie.movie_id, "actor": actor},
                )
    finally:
        db.close()