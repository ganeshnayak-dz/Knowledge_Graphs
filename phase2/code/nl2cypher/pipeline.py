"""NL → Cypher → Neo4j. Uses get_llm() and prompts; schema loaded from file (see scripts/generate_schema.py)."""

from typing import Any

from core.config import get_schema_path
from db.connection import Neo4jConnection
from llm import get_llm

from nl2cypher.prompts import SYSTEM_PROMPT
from nl2cypher.cypher_utils import extract_cypher, is_read_only


def load_schema_text() -> str:
    """Load schema from nl2cypher/prompt_schema/graph_schema.txt. Run scripts/generate_schema.py if missing."""
    path = get_schema_path()
    if not path.exists():
        raise FileNotFoundError(
            f"Schema file not found: {path}. Run from phase2/code: python scripts/generate_schema.py"
        )
    return path.read_text(encoding="utf-8").strip()


def ask_graph(question: str,verbose:bool=False) -> list[dict[str, Any]]:
    schema_text = load_schema_text()
    llm = get_llm()
    raw = llm.generate(SYSTEM_PROMPT + "\n\n" + schema_text, question)
    if verbose:
        print("--------------------------------")
        print(f"Raw Cypher: {raw}")
        print("--------------------------------")
        
    cypher = extract_cypher(raw)
    if not cypher:
        raise ValueError("No Cypher found in LLM response")
    if not is_read_only(cypher):
        raise ValueError("Only read-only Cypher is allowed")
    
    if verbose:
        print("--------------------------------")
        print(f"Generated Cypher: {cypher}")
        print("--------------------------------")
    
    db=Neo4jConnection()
    try:
        records = db.execute_query(cypher)
        results= [r.data() if hasattr(r, "data") else dict(r) for r in records]
        return {"query": cypher, "results": results}
    finally:
        db.close()