import http.server
import socketserver
import json
import sys

# This is the port we defined in your client
PORT = 8000

class RequestSpyHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. Identify the address the request was sent to
        if self.path == '/api/search':
            self._handle_search()
        else:
            self.send_error(404, "Endpoint not found")

    def _handle_search(self):
        # 2. Reading the information sent from the client (your client)
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            # Convert the data to JSON and print it nicely to the screen
            json_payload = json.loads(post_data.decode('utf-8'))
            
            print("\n" + "="*40)
            print(f"📡 RECEIVED REQUEST AT: {self.path}")
            print("="*40)
            print(json.dumps(json_payload, indent=4, ensure_ascii=False))
            print("="*40 + "\n")

            # 3. Return a valid response (so the client continues to work)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Prepare a dummy response that matches the structure in types.py
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
            
            # Sending the response
            response_json = json.dumps(dummy_response, indent=4)
            print("\n" + "-"*40)
            print("📤 SENDING RESPONSE:")
            print("-"*40)
            print(response_json)
            print("-"*40 + "\n")
            self.wfile.write(response_json.encode('utf-8'))
            
        except json.JSONDecodeError:
            print("❌ Error: Received data is not valid JSON")
            self.send_error(400, "Invalid JSON")

# Defining the server
with socketserver.TCPServer(("", PORT), RequestSpyHandler) as httpd:
    print(f"🕵️  Spy Server is running at http://localhost:{PORT}")
    print("Waiting for requests from your app...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
        httpd.server_close()
        sys.exit()