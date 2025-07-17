from graphiti.graph import Graph
from graphiti.llm import LLM

def get_graph(config: dict) -> Graph:
    """Initializes the Graphiti graph from a config."""
    return Graph(config)

def get_llm(config: dict) -> LLM:
    """Initializes the Graphiti LLM from a config."""
    return LLM(config) 