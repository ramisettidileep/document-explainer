from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAnalyzer(ABC):
    def __init__(self, ollama_client=None):
        self.ollama = ollama_client

    @abstractmethod
    def analyze(self, normalized_doc: Dict[str, Any]) -> Dict[str, Any]:
        pass