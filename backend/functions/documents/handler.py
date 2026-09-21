from backend.functions.documents.app import handle_document_request

def lambda_handler(event, context):
    return handle_document_request(event)