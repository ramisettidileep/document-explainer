"""Intelligent grounded Q&A handler with entity lookup and Ollama synthesis."""
import json
import re
from backend.services.storage.documents import DocumentStore
from backend.services.authorization.policy import is_authorized
from backend.services.ollama.client import OllamaClient

store = DocumentStore()
ollama = OllamaClient()

def lambda_handler(event, context):
    headers = event.get("headers") or {}
    user_id = headers.get("x-user-id") or headers.get("X-User-Id", "demo-user")
    path = event.get("path") or event.get("rawPath", "")

    parts = path.strip("/").split("/")
    if len(parts) < 3 or parts[0] != "documents" or parts[2] != "chat":
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid route."})}

    doc_id = parts[1]
    doc = store.get(doc_id)
    if not doc:
        return {"statusCode": 404, "body": json.dumps({"error": "Document not found."})}

    if not is_authorized(user_id, "ChatDocument", doc.get("owner")):
        return {"statusCode": 403, "body": json.dumps({"error": "Forbidden."})}

    body = json.loads(event.get("body") or "{}")
    question = body.get("question", "").strip()

    if not question:
        return {"statusCode": 400, "body": json.dumps({"error": "Question cannot be empty."})}

    raw_text = doc["parsed"]["text"]
    key_fields = doc.get("result", {}).get("key_fields", [])
    q_lower = question.lower()

    # 1. First, check key fields for direct precision matches
    direct_match = None
    for field in key_fields:
        label = field.get("label", "").lower()
        if label and (label in q_lower or any(word in q_lower for word in label.split() if len(word) > 3)):
            ref_str = f" (Reference Range: {field['reference_range']})" if field.get("reference_range") and field['reference_range'] != "Not stated" else ""
            status_str = f" - Status: {field['status']}" if field.get("status") else ""
            direct_match = f"According to the document, {field['label']} is recorded as {field['value']}{ref_str}{status_str}."
            break

    if direct_match:
        answer = direct_match
    elif ollama.is_available():
        # 2. If Ollama is available, generate grounded synthesis
        prompt = (
            f"You are a helpful document assistant. Answer the question using ONLY the provided document text. "
            f"If the answer is not in the document, state 'I could not find that information in the document.' "
            f"Keep your answer to 1-2 factual sentences.\n\n"
            f"Document:\n{raw_text[:1800]}\n\n"
            f"Question: {question}\nAnswer:"
        )
        llm_answer = ollama.generate(prompt)
        answer = llm_answer.strip() if llm_answer else "I couldn't locate specific information addressing that question in the document."
    else:
        # 3. Grounded sentence extraction fallback
        sentences = re.split(r'\. |\n', raw_text)
        matched_sentences = [s.strip() for s in sentences if any(w in s.lower() for w in q_lower.split() if len(w) > 3)]
        if matched_sentences:
            answer = f"The document notes: \"{matched_sentences[0]}\""
        else:
            answer = "I could not find that specific information in the uploaded document."

    evidence = doc.get("result", {}).get("evidence", [])[:2]

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,X-User-Id"
        },
        "body": json.dumps({
            "answer": answer,
            "evidence": evidence
        })
    }