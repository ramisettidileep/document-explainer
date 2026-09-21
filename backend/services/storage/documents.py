"""Document store matching persistence contract."""
import time
from typing import Dict, Any, Optional, List

class DocumentStore:
    _instance = None
    _storage: Dict[str, Dict[str, Any]] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DocumentStore, cls).__new__(cls)
            cls._storage = {}
        return cls._instance

    def save(self, doc_id: str, document_data: Dict[str, Any]) -> None:
        document_data["updated_at"] = int(time.time())
        self._storage[doc_id] = document_data

    def get(self, doc_id: str) -> Optional[Dict[str, Any]]:
        return self._storage.get(doc_id)

    def list_by_owner(self, owner: str) -> List[Dict[str, Any]]:
        return [
            {
                "id": doc["id"],
                "owner": doc.get("owner"),
                "created_at": doc.get("created_at"),
                "status": doc.get("status"),
                "document_type": doc.get("document_type", "general"),
                "summary": doc.get("result", {}).get("summary", "Ready") if doc.get("result") else "Pending"
            }
            for doc in self._storage.values()
            if doc.get("owner") == owner or owner == "admin"
        ]

    def delete(self, doc_id: str) -> bool:
        if doc_id in self._storage:
            del self._storage[doc_id]
            return True
        return False