"""Tree-structured Index Data Structures."""

# indices
from llama_index.indices.tree.base import GPTTreeIndex
from llama_index.indices.tree.embedding_query import GPTTreeIndexEmbeddingQuery
from llama_index.indices.tree.leaf_query import GPTTreeIndexLeafQuery
from llama_index.indices.tree.retrieve_query import GPTTreeIndexRetQuery

__all__ = [
    "GPTTreeIndex",
    "GPTTreeIndexLeafQuery",
    "GPTTreeIndexRetQuery",
    "GPTTreeIndexEmbeddingQuery",
]
