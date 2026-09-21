import json
import traceback
from http.server import HTTPServer, BaseHTTPRequestHandler
from backend.functions.documents.app import handle_document_request

class LocalAPIHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-User-Id, Authorization")
        self.send_header("Access-Control-Allow-Methods", "OPTIONS, GET, POST, DELETE")

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def _handle_request(self, method):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body_str = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"

            event = {
                "httpMethod": method,
                "path": self.path.split("?")[0],
                "headers": dict(self.headers),
                "body": body_str
            }

            response = handle_document_request(event)
            status_code = response.get("statusCode", 200)
            headers = response.get("headers", {})
            body = response.get("body", "{}")

            self.send_response(status_code)
            self._send_cors_headers()
            for k, v in headers.items():
                if k.lower() not in ["access-control-allow-origin", "access-control-allow-headers", "access-control-allow-methods"]:
                    self.send_header(k, v)
            self.end_headers()
            self.wfile.write(body.encode("utf-8"))

        except Exception as e:
            traceback.print_exc()
            self.send_response(500)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"Internal server error: {str(e)}"}).encode("utf-8"))

    def do_GET(self): self._handle_request("GET")
    def do_POST(self): self._handle_request("POST")
    def do_DELETE(self): self._handle_request("DELETE")

if __name__ == "__main__":
    PORT = 3000
    print(f"🚀 Document Explainer Local Server running at http://127.0.0.1:{PORT}")
    server = HTTPServer(("127.0.0.1", PORT), LocalAPIHandler)
    server.serve_forever()