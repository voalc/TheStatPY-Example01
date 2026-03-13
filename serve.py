import http.server
import socketserver
import webbrowser
import os

PORT = 1342  # You can change this port if needed
DIRECTORY = "./src"  # Change this to the directory you want to serve

# Change working directory to the folder you want to serve
os.chdir(DIRECTORY)

# Handler to serve files
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    url = f"http://localhost:{PORT}/"
    print(f"Serving at {url}")
    
    # Open the default web browser
    webbrowser.open(url)
    
    # Start the server
    httpd.serve_forever()
