from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain

from graph.connection import get_graph
from llm import get_llm_for_chain

def get_qa_chain(verbose:bool=True) -> GraphCypherQAChain:
    """Build GraphCypherQAChain for NL2Cypher."""
    llm=get_llm_for_chain()
    graph=get_graph()
    return GraphCypherQAChain.from_llm(llm=llm,
     graph=graph, 
     verbose=verbose, 
     allow_dangerous_requests=True)

def ask_graph(question:str,verbose:bool=True) -> dict:
    "Ask a question about the graph."
    chain=get_qa_chain(verbose=verbose)
    return chain.invoke({"query": question})