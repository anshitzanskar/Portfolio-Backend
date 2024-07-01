# server.py
import http.server
import socketserver
import json
import os
from pathlib import Path
from datetime import datetime

PORT = 3000
DIRECTORY = f"{Path.home()}/Portfolio-Backend/portfolios"

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path == '/portf-files':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            today_date = datetime.now().strftime('%Y%m%d')
            files = [f for f in os.listdir(DIRECTORY) if f.endswith(f'_{today_date}.json')]
            self.wfile.write(json.dumps(files).encode())
        else:
            super().do_GET()

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
                                                                                                                        