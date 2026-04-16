import http.server
import socketserver
import webbrowser
import os, subprocess

from adminonly.cli_alyod_text import cl
from process_thestatpy import process_thestatpy

PORT = 1342  # You can change this port if needed
DIRECTORY = "./src"  # Change this to the directory you want to serve

# Change working directory to the folder you want to serve
os.chdir(DIRECTORY)

class TheStatPyDevHandler(http.server.SimpleHTTPRequestHandler):
    """Serve HTML files after resolving <thestatpy> components in development."""

    def do_GET(self):
        requested_path = self.path.split("?", 1)[0].split("#", 1)[0]
        file_path = self.translate_path(requested_path)

        if os.path.isdir(file_path):
            file_path = os.path.join(file_path, "index.html")

        if os.path.isfile(file_path) and file_path.lower().endswith(".html"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                processed_content = process_thestatpy(content, os.path.dirname(file_path))
                payload = processed_content.encode("utf-8")

                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)
                return
            except Exception as exc:
                self.send_error(500, f"TheStatPy processing failed: {exc}")
                return

        super().do_GET()


Handler = TheStatPyDevHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        subprocess.run("cls" if os.name == "nt" else 'clear', shell=True)
        print(cl.align("DASHBOARD (dev version)", 50, "center", "bold","bg_blue", "white"))
        print(cl.align("STATUS: ONLINE", 50, "right", "green", "bold"))

        print(f"{cl.align('Port', 15, 'left', 'cyan', 'underline')} | {cl.align('Serving URL', 30, 'center', 'white', 'dim')}")
        print(f"{cl.align(str(PORT), 15, 'left')} | {cl.align(f'http://127.0.0.1:{PORT}', 30, 'center', 'yellow')}\n")
        print(cl.align('HTTPD LOGS', 40, 'center'))
        
        # Open the default web browser
        webbrowser.open(f"http://localhost:{PORT}")
        httpd.serve_forever()
    except KeyboardInterrupt:
        subprocess.run("cls" if os.name == "nt" else 'clear', shell=True)

        print(cl.align("DASHBOARD (dev version)", 50, "center", "bold","bg_blue", "white"))
        print(cl.align("STATUS: OFFLINE", 50, "right", "red", "bold"))
        print(f"{cl.align('Port', 15, 'left', 'cyan', 'underline')} | {cl.align('Serving URL', 30, 'center', 'white', 'dim')}")
        print(f"{cl.align(str(PORT), 15, 'left')} | {cl.align(f'http://127.0.0.1:{PORT}', 30, 'center', 'yellow')}\n")


        print("\nShutting down server...")
        httpd.shutdown()
        print("Server stopped.", "\n"*2)
    except Exception as e:
        print("Error Detected:\t", e)