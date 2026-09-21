"""Modular OpenSearch client stub."""
import os

class OpenSearchClient:
    def __init__(self, endpoint: str = None):
        self.endpoint = endpoint or os.environ.get("OPENSEARCH_URL", "http://localhost:9200")

    def index_document(self, doc_id: str, text: str) -> bool:
        return True

    def search_similar(self, query: str, top_k: int = 3) -> list:
        return []