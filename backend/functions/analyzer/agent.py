from backend.functions.documents.app import ANALYZERS

def analyze_document_payload(doc_type: str, parsed_doc: dict) -> dict:
    analyzer = ANALYZERS.get(doc_type, ANALYZERS["general"])
    return analyzer.analyze(parsed_doc)