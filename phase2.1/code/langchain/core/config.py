"""Configuration (Neo4j, API keys, paths). Fill as you learn."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    neo4j_uri: str
    neo4j_user: str
    neo4j_password: str
    neo4j_db: str

    llm_provider: str = "groq"
    groq_api_key: Optional[str] = None
    groq_model: Optional[str] = None
    # schema_file: str = "nl2cypher/prompt_schema/graph_schema.txt"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()