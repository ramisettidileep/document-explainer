import json
import uuid
import time
from backend.utils.parsing import parse_raw_text
from backend.functions.classifier.classifier import DocumentClassifier
from backend.services.storage.documents import DocumentStore
from backend.services.authorization.policy import is_authorized
from backend.functions.chat.handler import lambda_handler as chat_lambda_handler
from backend.analyzers.medical import MedicalAnalyzer
from backend.analyzers.banking import BankingAnalyzer
from backend.analyzers.legal import LegalAnalyzer
from backend.analyzers.insurance import InsuranceAnalyzer
from backend.analyzers.financial import FinancialAnalyzer
from backend.analyzers.utility import UtilityAnalyzer
from backend.analyzers.general import GeneralAnalyzer

store = DocumentStore()
classifier = DocumentClassifier()

ANALYZERS = {
    "medical": MedicalAnalyzer(),
    "banking": BankingAnalyzer(),
    "legal": LegalAnalyzer(),
    "insurance": InsuranceAnalyzer(),
    "financial": FinancialAnalyzer(),
    "utility": UtilityAnalyzer(),
    "general": GeneralAnalyzer()
}

def make_response(status_code: int, body: dict):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,X-User-Id,Authorization",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,DELETE"
        },
        "body": json.dumps(body)
    }

def handle_document_request(event):
    http_method = event.get("httpMethod") or event.get("requestContext", {}).get("http", {}).get("method")
    path = event.get("path") or event.get("rawPath", "")
    headers = event.get("headers") or {}
    user_id = headers.get("x-user-id") or headers.get("X-User-Id", "demo-user")

    if http_method == "OPTIONS":
        return make_response(200, {"status": "ok"})

    # 1. POST /documents/{id}/chat  <-- (FIXED: Route chat calls directly to chat handler)
    if http_method == "POST" and "/documents/" in path and path.endswith("/chat"):
        return chat_lambda_handler(event, None)

    # 2. POST /documents (Create document)
    if http_method == "POST" and path.rstrip("/") == "/documents":
        if not is_authorized(user_id, "CreateDocument", user_id):
            return make_response(403, {"error": "Unauthorized action."})

        body = json.loads(event.get("body") or "{}")
        raw_text = body.get("text", "")
        if not raw_text.strip():
            return make_response(400, {"error": "Document text cannot be empty."})

        doc_id = str(uuid.uuid4())
        parsed = parse_raw_text(raw_text, body.get("file_name", "upload.txt"))
        classification = classifier.classify(raw_text)
        dtype = classification["document_type"]

        analyzer = ANALYZERS.get(dtype, ANALYZERS["general"])
        analysis_result = analyzer.analyze(parsed)

        record = {
            "id": doc_id,
            "owner": body.get("owner", user_id),
            "created_at": int(time.time()),
            "status": "complete",
            "document_type": dtype,
            "classification": classification,
            "parsed": parsed,
            "result": analysis_result
        }
        store.save(doc_id, record)
        return make_response(201, {"id": doc_id, "status": "complete"})

    # 3. GET /documents (List documents)
    if http_method == "GET" and path.rstrip("/") == "/documents":
        return make_response(200, {"documents": store.list_by_owner(user_id)})

    # 4. GET /documents/{id} (Get document details)
    if http_method == "GET" and "/documents/" in path and not path.endswith("/chat"):
        doc_id = path.rstrip("/").split("/")[-1]
        doc = store.get(doc_id)
        if not doc:
            return make_response(404, {"error": "Document not found."})
        if not is_authorized(user_id, "GetDocument", doc.get("owner")):
            return make_response(403, {"error": "Forbidden."})
        return make_response(200, doc)

    # 5. DELETE /documents/{id} (Delete document)
    if http_method == "DELETE" and "/documents/" in path:
        doc_id = path.rstrip("/").split("/")[-1]
        doc = store.get(doc_id)
        if not doc:
            return make_response(404, {"error": "Document not found."})
        if not is_authorized(user_id, "DeleteDocument", doc.get("owner")):
            return make_response(403, {"error": "Forbidden."})
        store.delete(doc_id)
        return make_response(200, {"status": "deleted", "id": doc_id})

    return make_response(404, {"error": f"Route not handled: {http_method} {path}"})