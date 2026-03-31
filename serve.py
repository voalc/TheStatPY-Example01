import http.server
import socketserver
import webbrowser
import os
from adminonly.cli_alyod_text import cl

PORT = 1342  # You can change this port if needed
DIRECTORY = "./src"  # Change this to the directory you want to serve

# Change working directory to the folder you want to serve
os.chdir(DIRECTORY)

# Handler to serve files
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    url = f"http://localhost:{PORT}/"
    print(cl.paint(f"Serving at {cl.paint(url, 'bold')}", "green"))
    
    # Open the default web browser
    webbrowser.open(url)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(cl.paint("\nShutting down server...", "yellow"))
        httpd.shutdown()
        print(cl.paint("Server stopped.", "red"), "\n"*2)