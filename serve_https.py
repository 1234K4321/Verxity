#!/usr/bin/env python3
"""
HTTPS server to serve the taskpane.html file on port 3000
This creates a self-signed certificate for local development.
For production, you'll need a proper SSL certificate.
"""

import http.server
import socketserver
import ssl
import os
from pathlib import Path

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

def create_self_signed_cert():
    """Create a self-signed certificate for local testing"""
    try:
        import subprocess
        
        # Create certificate if it doesn't exist
        if not (Path("server.crt").exists() and Path("server.key").exists()):
            print("Creating self-signed certificate for HTTPS...")
            subprocess.run([
                "openssl", "req", "-x509", "-newkey", "rsa:4096", "-keyout", "server.key",
                "-out", "server.crt", "-days", "365", "-nodes",
                "-subj", "/C=US/ST=State/L=City/O=Organization/CN=localhost"
            ], check=True)
            print("Certificate created successfully!")
        
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("OpenSSL not found or certificate creation failed.")
        print("Please install OpenSSL or create certificates manually.")
        return False

if __name__ == "__main__":
    # Try to create HTTPS server
    use_https = create_self_signed_cert()
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        if use_https and Path("server.crt").exists() and Path("server.key").exists():
            # Set up SSL context
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain("server.crt", "server.key")
            httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
            
            print(f"Serving taskpane.html with HTTPS at https://localhost:{PORT}")
            print(f"Your taskpane.html will be available at https://localhost:{PORT}/taskpane.html")
            print("Note: You may need to accept the self-signed certificate warning in your browser.")
        else:
            print(f"Serving taskpane.html with HTTP at http://localhost:{PORT}")
            print(f"Your taskpane.html will be available at http://localhost:{PORT}/taskpane.html")
            print("Warning: HTTPS is required for production deployment.")
        
        print("Press Ctrl+C to stop the server.")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down the server...")
            httpd.shutdown()
