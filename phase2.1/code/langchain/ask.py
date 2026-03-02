"""CLI: ask a natural-language question about the graph (NL→Cypher via GraphCypherQAChain)."""
from nl2cypher.chain import ask_graph

VERBOSE = True  # set to False to hide generated Cypher


def main():
    print("Ask questions about the graph. Type 'exit' or 'quit' to stop.\n")
    while True:
        try:
            question = input("You: ").strip()
            if not question or question.lower() in ("exit", "quit"):
                break
            response = ask_graph(question, verbose=VERBOSE)
            # Chain returns {"result": "..."}; show result when present, else full response
            answer = response.get("result", response)
            print(answer)
            print()
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
