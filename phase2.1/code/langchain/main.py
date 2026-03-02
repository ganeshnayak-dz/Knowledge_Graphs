"""Run movie ingest: load CSV and write to Neo4j. Run from phase2.1/code/langchain with data/ one level up."""
from pathlib import Path

from ingest.load_data import ingest_movies


def _default_data_path() -> Path:
    """Movie CSV next to code/langchain (e.g. phase2.1/data/movie.csv)."""
    return Path(__file__).resolve().parent.parent.parent / "data" / "movie.csv"


if __name__ == "__main__":
    path = _default_data_path()
    if not path.exists():
        print(f"Data file not found: {path}")
        print("Usage: python main.py   (expects ../../data/movie.csv) or pass path as needed.")
        exit(1)
    ingest_movies(str(path))
    print("Ingest done.")