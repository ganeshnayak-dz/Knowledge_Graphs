"""Load and parse source data (CSV, JSON, etc.) from data/. Fill as you learn."""
import pandas as pd
from db.connection import Neo4jConnection
from graph import schema
from models.movie import MovieModel




def ingest_movies(file_path:str):

    df=pd.read_csv(file_path)
    db=Neo4jConnection()

    for constraint in schema.CREATE_CONSTRAINS:
        db.execute(constraint)
    
    for _,row in df.iterrows():
        try:
            movie=MovieModel(**row.to_dict())
        except Exception as e:
            print(f"Validation failed:{e}")
            continue
    
        # Movie
        db.execute(schema.CREATE_MOVIE,movie.model_dump())

        # Genres
        for genre in movie.genre:
            db.execute(schema.CREATE_GENRE_REL,
            {"movie_id":movie.movie_id,
            "genre":genre})
        
        # Director
        db.execute(schema.CREATE_DIRECTOR_REL, {
            "movie_id": movie.movie_id,
            "director": movie.director
        })

        # Actors
        for actor in movie.cast:
            db.execute(schema.CREATE_ACTOR_REL, {
                "movie_id": movie.movie_id,
                "actor": actor
            })

    db.close()