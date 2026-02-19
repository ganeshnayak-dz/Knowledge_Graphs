"""Extract and validate Cypher from LLM output. No LLM-specific code."""
import re


def extract_cypher(text: str) -> str | None:
    """Get Cypher from LLM reply (handles markdown code blocks or plain text)."""
    text = (text or "").strip()
    # Try markdown code block first: ```cypher ... ``` or ``` ... ```
    m = re.search(r"```(?:cypher)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()
    # Otherwise use first line that looks like Cypher
    lines = text.split("\n")
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped and stripped.upper().startswith(("MATCH", "RETURN")):
            return "\n".join(lines[i:]).strip()
    return text if text else None


def is_read_only(cypher: str) -> bool:
    """Allow only read-style Cypher (no CREATE, MERGE, DELETE, etc.)."""
    forbidden = ("CREATE", "MERGE", "DELETE", "SET", "REMOVE", "DROP")
    return not any(f in cypher.upper() for f in forbidden)
