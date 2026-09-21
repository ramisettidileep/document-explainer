from backend.analyzers.base import BaseAnalyzer

class GeneralAnalyzer(BaseAnalyzer):
    def analyze(self, normalized_doc):
        text = normalized_doc["text"]
        return {
            "doc_type": "general",
            "summary": text[:250] + ("..." if len(text) > 250 else ""),
            "key_fields": [
                {"label": "Word Count", "value": str(len(text.split()))},
                {"label": "Total Pages", "value": str(normalized_doc.get("total_pages", 1))}
            ],
            "flags": [{"type": "info", "message": "General document without domain-specific schema."}],
            "action_items": [{"action": "Review document details.", "grounded_reason": "General inspection."}],
            "evidence": [{"claim": "Document ingested successfully", "source": {"page": 1, "section": "Body", "text": text[:60]}}],
            "calculations": []
        }