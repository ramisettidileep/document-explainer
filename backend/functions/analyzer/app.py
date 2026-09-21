import json
from backend.functions.analyzer.agent import analyze_document_payload

def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    res = analyze_document_payload(body.get("doc_type", "general"), body.get("parsed", {}))
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(res)
    }