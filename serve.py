import http.server
import socketserver
import webbrowser
import os, subprocess

from adminonly.cli_alyod_text import cl

PORT = 1342  # You can change this port if needed
DIRECTORY = "./src"  # Change this to the directory you want to serve

# Change working directory to the folder you want to serve
os.chdir(DIRECTORY)

# Handler to serve files
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        subprocess.run("cls" if os.name == "nt" else 'clear', shell=True)
        print(cl.align("DASHBOARD (dev version)", 50, "center", "bold","bg_blue", "white"))
        print(cl.align("STATUS: ONLINE", 50, "right", "green", "bold"))

        print(f"{cl.align("Port", 15, "left", "cyan", "underline")} | {cl.align("Serving URL", 30, "center", "white", "dim")}")
        print(f"{cl.align(str(PORT), 15, 'left')} | {cl.align(f'http://127.0.0.1:{PORT}', 30, 'center', 'yellow')}\n")
        print(cl.align('HTTPD LOGS', 40, 'center'))
        
        # Open the default web browser
        webbrowser.open(f"http://localhost:{PORT}")
        httpd.serve_forever()
    except KeyboardInterrupt:
        subprocess.run("cls" if os.name == "nt" else 'clear', shell=True)

        print(cl.align("DASHBOARD (dev version)", 50, "center", "bold","bg_blue", "white"))
        print(cl.align("STATUS: OFFLINE", 50, "right", "red", "bold"))
        print(f"{cl.align("Port", 15, "left", "cyan", "underline")} | {cl.align("Serving URL", 30, "center", "white", "dim")}")
        print(f"{cl.align(str(PORT), 15, 'left')} | {cl.align(f'http://127.0.0.1:{PORT}', 30, 'center', 'yellow')}\n")


        print("\nShutting down server...")
        httpd.shutdown()
        print("Server stopped.", "\n"*2)
    except Exception as e:
        print("Error Detected:\t", e)