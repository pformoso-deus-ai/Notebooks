import pytest
from langchain_core.documents import Document
from domain.graph import NodeLabel, RelationshipType

pytestmark = pytest.mark.asyncio


async def test_transform_simple_text(llm_transformer):
    """Test transforming a simple text into a graph"""
    doc = Document(page_content="The developer agent created a new task to implement a user authentication system.")
    graph_docs = await llm_transformer.transform([doc])
    
    assert len(graph_docs) == 1
    plan = graph_docs[0]
    assert len(plan.nodes) > 0
    assert len(plan.relationships) > 0
    assert any(node.label.value == "Agent" for node in plan.nodes)
    assert any(node.label.value == "Task" for node in plan.nodes)


async def test_transform_multiple_documents(llm_transformer):
    """Test transforming multiple documents into a graph"""
    docs = [
        Document(page_content="The developer agent created a new task to implement user authentication."),
        Document(page_content="The architect agent discussed the OAuth2 concept with the developer."),
        Document(page_content="The developer implemented a solution using JWT tokens."),
    ]

    graph_docs = await llm_transformer.transform(docs)
    
    assert len(graph_docs) == 3
    all_nodes = [node for gd in graph_docs for node in gd.nodes]
    all_rels = [rel for gd in graph_docs for rel in gd.relationships]
    
    assert len(all_nodes) > 3
    assert len(all_rels) > 2


async def test_transform_empty_document(llm_transformer):
    """Test that transforming an empty document returns an empty list."""
    docs = [Document(page_content="")]
    graph_docs = await llm_transformer.transform(docs)
    assert len(graph_docs) == 1 # The transformer might still produce a GraphDocument wrapper
    assert len(graph_docs[0].nodes) == 0
    assert len(graph_docs[0].relationships) == 0


@pytest.mark.skip(reason="This test depends on a live API call and LLM behavior is not deterministic for irrelevant text.")
async def test_transform_irrelevant_text(llm_transformer):
    """Test that transforming irrelevant text doesn't produce meaningful domain nodes."""
    docs = [Document(page_content="The weather is nice today.")]
    graph_docs = await llm_transformer.transform(docs)
    
    assert len(graph_docs) == 1
    plan = graph_docs[0]
    
    # The LLM might still extract generic concepts, but it shouldn't extract our specific domain labels.
    domain_labels = {label.value for label in NodeLabel}
    extracted_labels = {node.label.value for node in plan.nodes}
    
    # Assert that there is no intersection between the extracted labels and our specific domain labels
    assert not (domain_labels & extracted_labels)
