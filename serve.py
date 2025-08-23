#!/usr/bin/env python3
"""
Simple HTTP server to serve the taskpane.html file on port 3000
Run this alongside your Flask app (app.py) to serve the frontend.
"""

import http.server
import socketserver
import os
import ssl

PORT = 3000
DIRECTORY = "."

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Add CORS headers to allow the add-in to work
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving taskpane.html at http://localhost:{PORT}")
        print(f"Your taskpane.html will be available at http://localhost:{PORT}/taskpane.html")
        print("For HTTPS (required for production), you'll need to set up SSL certificates.")
        print("Press Ctrl+C to stop the server.")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down the server...")
            httpd.shutdown()
