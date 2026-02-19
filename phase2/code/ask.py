from nl2cypher import ask_graph

VERBOSE = True  # set to False to hide generated Cypher

def main():
    print("Ask questions about the graph. Type 'exit' or 'quit' to stop.\n")
    while True:
        try:
            question = input("You: ").strip()
            if not question or question.lower() in ("exit", "quit"):
                break
            out = ask_graph(question, verbose=VERBOSE)
            print(f"Query: {out['query']}\n")   # always show query, or only when VERBOSE
            print("Results:")
            for row in out["results"]:
                print(row)
            print()
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    main()