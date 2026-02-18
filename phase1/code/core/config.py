from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    neo4j_uri:str
    neo4j_user:str
    neo4j_password:str
    neo4j_db:str

    class Config:
        env_file='.env'
        extra='ignore'
        

settings=Settings()
