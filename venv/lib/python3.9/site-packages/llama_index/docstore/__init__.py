from llama_index.docstore.types import BaseDocumentStore
from llama_index.docstore.simple_docstore import SimpleDocumentStore

# alias for backwards compatibility
from llama_index.docstore.simple_docstore import DocumentStore
from llama_index.docstore.mongo_docstore import MongoDocumentStore


__all__ = [
    "BaseDocumentStore",
    "SimpleDocumentStore",
    "DocumentStore",
    "MongoDocumentStore",
]
