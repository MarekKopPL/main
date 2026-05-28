import json
from http.server import BaseHTTPRequestHandler, HTTPServer

import vertexai
from vertexai.generative_models import GenerativeModel

# Initialize Vertex AI
vertexai.init(
    project="gen-lang-client-0041373390",
    location="us-central1"
)

model = GenerativeModel("gemini-1.5-pro")

class VertexAIRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        if self.path == "/":
            self._set_headers()
            self.wfile.write(json.dumps({"status": "ok", "message": "Vertex AI REST endpoint is running."}).encode())
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        if self.path != "/generate":
            self.send_error(404, "Not Found")
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            payload = json.loads(body or b"{}")
            prompt = payload.get("prompt", "Explain AI in 1 sentence")
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return

        try:
            response = model.generate_content(prompt)
            result = {
                "prompt": prompt,
                "text": response.text,
            }
            self._set_headers(200)
            self.wfile.write(json.dumps(result).encode())
        except Exception as exc:
            self.send_error(500, f"Model request failed: {exc}")

if __name__ == "__main__":
    server_address = ("0.0.0.0", 8080)
    httpd = HTTPServer(server_address, VertexAIRequestHandler)
    print("Starting Vertex AI REST API on http://0.0.0.0:8080")
    print("POST /generate with JSON {\"prompt\": \"your prompt\"}")
    httpd.serve_forever()
