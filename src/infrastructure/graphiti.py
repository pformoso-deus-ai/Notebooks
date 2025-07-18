from graphiti_core import Graphiti

def get_graphiti(config: dict) -> Graphiti:
    """Initializes the Graphiti instance from a config."""
    return Graphiti(
        uri=config.get("uri"),
        user=config.get("user"),
        password=config.get("password"),
        # Add more config as needed (llm_client, embedder, etc.)
    ) 