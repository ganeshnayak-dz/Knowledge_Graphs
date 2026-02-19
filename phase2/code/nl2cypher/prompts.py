"""Single place for all NL→Cypher prompt text. Schema is loaded from nl2cypher/prompt_schema/graph_schema.txt (see scripts/generate_schema.py)."""

SYSTEM_PROMPT = (
    "You are a Cypher expert. Given the graph schema and a question, reply with ONLY one Cypher READ query. "
    "Use only MATCH, RETURN, WHERE, WITH, ORDER BY, LIMIT. No CREATE/MERGE/DELETE. No explanation."
)