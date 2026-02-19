"""
Generate graph schema from Neo4j and save to nl2cypher/prompt_schema/graph_schema.txt.
Run this when the graph structure changes; the pipeline uses the saved file for every question.

Includes node labels, their properties, and relationship structure so the LLM can generate accurate Cypher.

Usage (from phase2/code):
    python scripts/generate_schema.py

Or:
    python -m scripts.generate_schema
"""
from collections import defaultdict
from pathlib import Path

from db.connection import Neo4jConnection


def _to_dicts(records: list) -> list[dict]:
    return [r.data() if hasattr(r, "data") else dict(r) for r in records]


def _get_labels(db: Neo4jConnection) -> list[str]:
    rows = db.execute_query("CALL db.labels() YIELD label RETURN label")
    return [r["label"] for r in _to_dicts(rows)]


def _get_node_properties(db: Neo4jConnection) -> dict[str, list[str]]:
    """
    Return label -> sorted list of property names.
    Tries Neo4j 5 db.schema.nodeTypeProperties(); falls back to sampling keys per label (Neo4j 4.x).
    """
    # Neo4j 5.x
    try:
        rows = db.execute_query(
            "CALL db.schema.nodeTypeProperties() YIELD nodeLabels, propertyName RETURN nodeLabels, propertyName"
        )
        rows = _to_dicts(rows)
        if rows:
            out: dict[str, list[str]] = defaultdict(list)
            for r in rows:
                labels = r.get("nodeLabels")
                prop = r.get("propertyName")
                if labels is not None and prop is not None:
                    label = labels[0] if isinstance(labels, list) else labels
                    out[label].append(prop)
            return {k: sorted(set(v)) for k, v in out.items()}
    except Exception:
        pass

    # Fallback (Neo4j 4.x or empty): sample one node per label and get keys(n)
    labels = _get_labels(db)
    out: dict[str, list[str]] = defaultdict(list)
    for label in labels:
        try:
            q = f"MATCH (n:`{label}`) RETURN keys(n) AS keys LIMIT 1"
            rows = db.execute_query(q)
            rows = _to_dicts(rows)
            if rows and rows[0].get("keys"):
                keys = rows[0]["keys"]
                out[label] = sorted(set(str(k) for k in keys))
        except Exception:
            out[label] = []
    return dict(out)


def _get_relationship_structure(db: Neo4jConnection) -> list[tuple[str, str, str]]:
    """Return list of (from_label, rel_type, to_label)."""
    q = """
    MATCH (a)-[r]->(b)
    WITH labels(a)[0] AS fromLabel, type(r) AS relType, labels(b)[0] AS toLabel
    RETURN DISTINCT fromLabel, relType, toLabel
    ORDER BY fromLabel, relType, toLabel
    """
    rows = db.execute_query(q)
    return [(r["fromLabel"], r["relType"], r["toLabel"]) for r in _to_dicts(rows)]


def build_schema_text(
    labels: list[str],
    rel_structure: list[tuple[str, str, str]],
    label_properties: dict[str, list[str]] | None = None,
) -> str:
    lines = ["Graph schema (Neo4j Cypher):"]
    if label_properties:
        node_parts = []
        for label in sorted(labels):
            props = label_properties.get(label)
            if props:
                node_parts.append(f"{label} ({', '.join(props)})")
            else:
                node_parts.append(label)
        lines.append("- Nodes: " + ", ".join(node_parts))
    else:
        lines.append("- Nodes: " + ", ".join(sorted(labels)))
    rel_parts = [f"({f})-[:{t}]->({to})" for f, t, to in rel_structure]
    lines.append("- Relationships: " + ", ".join(rel_parts))
    return "\n".join(lines)


def main() -> None:
    code_root = Path(__file__).resolve().parent.parent
    schema_dir = code_root / "nl2cypher" / "prompt_schema"
    schema_file = schema_dir / "graph_schema.txt"
    schema_dir.mkdir(parents=True, exist_ok=True)

    db = Neo4jConnection()
    try:
        labels = _get_labels(db)
        label_properties = _get_node_properties(db)
        rel_structure = _get_relationship_structure(db)
        if not labels:
            print("Warning: no labels found in the database. Schema may be empty.")
        text = build_schema_text(labels, rel_structure, label_properties)
        schema_file.write_text(text, encoding="utf-8")
        print(f"Schema written to {schema_file}")
        print("---")
        print(text)
    finally:
        db.close()


if __name__ == "__main__":
    main()
