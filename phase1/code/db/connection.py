import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

uri = os.getenv("NEO4J_URI").strip()
username = os.getenv("NEO4J_USERNAME").strip()
password = os.getenv("NEO4J_PASSWORD").strip()
database = os.getenv("NEO4J_DATABASE").strip()

driver = GraphDatabase.driver(uri, auth=(username, password))

def check_connection():
    try:
        driver.verify_connectivity()
        print("Connected to Neo4j successfully.")
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False
    finally:
        driver.close()
