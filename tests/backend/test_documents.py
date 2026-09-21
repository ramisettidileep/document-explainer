import unittest
import json
from backend.functions.documents.app import handle_document_request

class TestDocuments(unittest.TestCase):
    def test_document_lifecycle(self):
        create_event = {
            "httpMethod": "POST",
            "path": "/documents",
            "headers": {"X-User-Id": "test-user"},
            "body": json.dumps({"text": "Subtotal: 100\nTax: 15\nTotal: 115", "file_name": "inv.txt"})
        }
        res = handle_document_request(create_event)
        self.assertEqual(res["statusCode"], 201)
        doc_id = json.loads(res["body"])["id"]

        get_event = {
            "httpMethod": "GET",
            "path": f"/documents/{doc_id}",
            "headers": {"X-User-Id": "test-user"}
        }
        res_get = handle_document_request(get_event)
        self.assertEqual(res_get["statusCode"], 200)

        unauth_get = {
            "httpMethod": "GET",
            "path": f"/documents/{doc_id}",
            "headers": {"X-User-Id": "other-user"}
        }
        res_unauth = handle_document_request(unauth_get)
        self.assertEqual(res_unauth["statusCode"], 403)

if __name__ == "__main__":
    unittest.main()