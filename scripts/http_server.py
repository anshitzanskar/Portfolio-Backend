# server.py
import os
import json
import logging
from pathlib import Path
from http import HTTPStatus
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

logging.basicConfig(level=logging.INFO)
logger= logging.getLogger(__name__)

PORT = 3000
DIRECTORY = f"{Path.home()}/Portfolio-Backend/portfolios"

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super(CORSRequestHandler, self).end_headers()

    def do_GET(self):
        if self.path == '/portfolioFiles':
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            today_date = datetime.now().strftime('%Y%m%d')
            files = [f for f in os.listdir(DIRECTORY) if f.endswith(f'_{today_date}.json')]
            self.wfile.write(json.dumps(files).encode())
        else:
            super().do_GET()

with HTTPServer(("", PORT), CORSRequestHandler) as httpd:
    logger.info(f"Serving at port {PORT}")
    httpd.serve_forever()
