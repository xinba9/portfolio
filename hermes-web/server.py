"""
Hermes Web Chat - Local Server with API Proxy (v3)
Uses requests library for robust encoding handling.
"""
import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests as req_lib
# Suppress SSL warnings (local proxy, acceptable tradeoff)
from requests.packages.urllib3.exceptions import InsecureRequestWarning
req_lib.packages.urllib3.disable_warnings(InsecureRequestWarning)

PORT = 8765

# API Configuration
API_BASE = "https://integrate.api.nvidia.com/v1"
API_KEY = "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"

HTML_CONTENT = open("index.html", "rb").read()


class ProxyHandler(BaseHTTPRequestHandler):
    """Handle all requests: serve HTML + proxy API calls"""

    def log_message(self, fmt, *args):
        print(f"[{self.log_date_time_string()}] {fmt % args}")

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(HTML_CONTENT)))
            self.end_headers()
            self.wfile.write(HTML_CONTENT)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def do_POST(self):
        if self.path == "/api/chat":
            self._proxy_chat()
        else:
            self.send_response(404)
            self.end_headers()

    def _proxy_chat(self):
        try:
            # Read request body
            content_length = int(self.headers.get("Content-Length", 0))
            body_bytes = self.rfile.read(content_length)
            body = json.loads(body_bytes) if body_bytes else {}

            model = body.get("model", "z-ai/glm-5.1")
            messages = body.get("messages", [])
            max_tokens = body.get("max_tokens", 2048)
            temperature = body.get("temperature", 0.7)
            stream = body.get("stream", True)

            print(f"[API] Request: model={model}, messages={len(messages)}, stream={stream}")

            payload = {
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": stream
            }

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}",
            }

            # Use requests for robust HTTP handling
            if stream:
                # Streaming response
                resp = req_lib.post(
                    f"{API_BASE}/chat/completions",
                    json=payload,
                    headers=headers,
                    stream=True,
                    timeout=90,
                    verify=False
                )

                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Connection", "close")
                self.end_headers()

                # Stream chunks to browser
                try:
                    for line in resp.iter_lines():
                        if line:
                            self.wfile.write(line + b"\n")
                            self.wfile.flush()
                except Exception as stream_err:
                    print(f"[API] Stream error (may be client disconnect): {stream_err}")

                print("[API] Streaming complete")

            else:
                # Non-streaming response
                resp = req_lib.post(
                    f"{API_BASE}/chat/completions",
                    json=payload,
                    headers=headers,
                    timeout=90,
                    verify=False
                )

                result = resp.json()
                reply_text = ""
                if "choices" in result and len(result["choices"]) > 0:
                    reply_text = result["choices"][0].get("message", {}).get("content", "")

                print(f"[API] Response: {reply_text[:100]}...")

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))

        except req_lib.exceptions.HTTPError as e:
            err_text = ""
            try:
                err_text = e.response.text[:500]
            except:
                pass
            print(f"[API] HTTP Error: {e} - {err_text}")
            self._send_error(e.response.status_code if e.response else 502, f"API Error: {err_text}")

        except req_lib.exceptions.ConnectionError as e:
            print(f"[API] Connection Error: {e}")
            self._send_error(502, f"Network error: Cannot connect to NVIDIA API. Check your internet connection.")

        except req_lib.exceptions.Timeout as e:
            print(f"[API] Timeout: {e}")
            self._send_error(504, "Request timed out. The API took too long to respond.")

        except Exception as e:
            err_msg = str(e)
            print(f"[API] Unexpected error: {err_msg}")
            import traceback
            traceback.print_exc()
            self._send_error(500, f"Server error: {err_msg}")

    def _send_error(self, code, message):
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        error_json = json.dumps({"error": {"message": message}}, ensure_ascii=False)
        self.wfile.write(error_json.encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def main():
    server = HTTPServer(("127.0.0.1", PORT), ProxyHandler)
    print(f"\n{'='*50}")
    print(f"  Hermes Web Chat Server v3")
    print(f"  http://localhost:{PORT}")
    print(f"{'='*50}\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        server.shutdown()


if __name__ == "__main__":
    main()
