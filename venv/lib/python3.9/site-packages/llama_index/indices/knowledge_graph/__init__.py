"""KG-based data structures."""

from llama_index.indices.knowledge_graph.base import GPTKnowledgeGraphIndex
from llama_index.indices.knowledge_graph.query import GPTKGTableQuery, KGQueryMode

__all__ = [
    "GPTKnowledgeGraphIndex",
    "GPTKGTableQuery",
    "KGQueryMode",
]
