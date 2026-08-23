import http.server
import socketserver
import webbrowser
import os
import sys

DEFAULT_PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def start_server():
    port = DEFAULT_PORT
    server = None
    for attempt in range(10):
        try:
            server = ReusableTCPServer(("", port), Handler)
            break
        except OSError as e:
            if e.errno == 10048 or "already in use" in str(e).lower():
                port += 1
            else:
                raise e

    if not server:
        print(f"Error: Could not bind to any port starting from {DEFAULT_PORT}")
        sys.exit(1)

    url = f"http://localhost:{port}"
    print(f"Starting server for Gujarati Std 1 Textbook app at {url}")
    try:
        webbrowser.open(url)
    except Exception:
        pass

    with server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    start_server()

