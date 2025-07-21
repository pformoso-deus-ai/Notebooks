from graphiti_core import Graphiti

async def get_graphiti(config: dict) -> Graphiti:
    """Initializes the Graphiti instance from a config and sets up indices."""
    graphiti = Graphiti(
        uri=config.get("uri"),
        user=config.get("user"),
        password=config.get("password"),
        # Add more config as needed (llm_client, embedder, etc.)
    )
    
    # Build indices and constraints for the database
    try:
        await graphiti.build_indices_and_constraints()
        print("✅ Graphiti indices and constraints built successfully")
    except Exception as e:
        print(f"⚠️  Warning: Could not build indices: {e}")
        print("   This is normal for the first run or if indices already exist")
    
    return graphiti 