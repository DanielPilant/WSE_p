import http.server
import socketserver
import json
import sys

PORT = 8000

class RequestSpyHandler(http.server.BaseHTTPRequestHandler):
    
    def _read_json(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        return json.loads(post_data.decode('utf-8'))

    def do_POST(self):
        if self.path == '/api/search':
            self._handle_search()
        elif self.path == '/api/cart/update':
            self._handle_cart_update()
        else:
            self.send_error(404, "Endpoint not found")

    def _handle_search(self):
        try:
            json_payload = self._read_json() 
            
            print("\n" + "="*40)
            print(f"🔎 SEARCH REQUEST: {self.path}")
            print(json.dumps(json_payload, indent=4, ensure_ascii=False))
            print("="*40)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            dummy_response = {
                "type": "result",
                "data": {
                    "store_name": "Spy Supermarket (Mock)",
                    "address": "Localhost Blvd 1",
                    "total_price": 45.90,
                    "items": [
                        {"id": "1", "name": "Spy Milk", "quantity": 1, "price": 10.90},
                        {"id": "2", "name": "Debug Eggs", "quantity": 1, "price": 35.00}
                    ]
                }
            }
            self.wfile.write(json.dumps(dummy_response).encode('utf-8'))
            
        except Exception as e:
            self.send_error(400, f"Error: {e}")

    def _handle_cart_update(self):
        try:
            json_payload = self._read_json() 
            
            print("\n" + "*"*40)
            print(f"🛒 CART UPDATE REQUEST: {self.path}")
            print("*"*40)
            print(json.dumps(json_payload, indent=4, ensure_ascii=False))
            print("*"*40 + "\n")

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            self.wfile.write(json.dumps({"status": "updated"}).encode('utf-8'))

        except Exception as e:
            self.send_error(400, f"Error: {e}")

with socketserver.TCPServer(("", PORT), RequestSpyHandler) as httpd:
    print(f"🕵️  Spy Server is running at http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        sys.exit()