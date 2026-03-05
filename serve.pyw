import os
import socket
import subprocess
import threading
import http.server
import socketserver
import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import signal
import time
import webbrowser

PORT = 1342
server_thread = None
watch_thread = None
httpd = None
watching = False
directory_snapshot = {}


# -------------------------
# Port Utilities
# -------------------------
def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def get_pid_using_port(port):
    try:
        if os.name == "nt":
            result = subprocess.check_output(
                f"netstat -ano | findstr :{port}",
                shell=True
            ).decode()
            lines = result.strip().split("\n")
            if lines:
                return lines[0].split()[-1]
        else:
            result = subprocess.check_output(
                f"lsof -i :{port} -sTCP:LISTEN -t",
                shell=True
            ).decode().strip()
            if result:
                return result
    except:
        pass
    return None


def force_kill_process(pid):
    try:
        if os.name == "nt":
            subprocess.call(f"taskkill /PID {pid} /F", shell=True)
        else:
            os.kill(int(pid), signal.SIGKILL)
        return True
    except:
        return False


# -------------------------
# Directory Monitoring
# -------------------------
def snapshot_directory(path):
    snap = {}
    for root, dirs, files in os.walk(path):
        for name in files:
            filepath = os.path.join(root, name)
            try:
                snap[filepath] = os.path.getmtime(filepath)
            except:
                pass
    return snap


def watch_directory(path):
    global directory_snapshot, watching

    directory_snapshot = snapshot_directory(path)

    while watching:
        time.sleep(2)
        new_snapshot = snapshot_directory(path)

        if new_snapshot != directory_snapshot:
            directory_snapshot = new_snapshot
            restart_server(path)


# -------------------------
# HTTP Server
# -------------------------
def run_server(directory):
    global httpd
    os.chdir(directory)
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), handler)
    httpd.serve_forever()


def start_hosting():
    global server_thread, watch_thread, watching

    if is_port_in_use(PORT):
        messagebox.showerror("Error", "Port already in use!")
        return

    directory = dir_path.get()
    if not os.path.isdir(directory):
        messagebox.showerror("Error", "Invalid directory.")
        return

    server_thread = threading.Thread(target=run_server, args=(directory,))
    server_thread.daemon = True
    server_thread.start()

    watching = True
    watch_thread = threading.Thread(target=watch_directory, args=(directory,))
    watch_thread.daemon = True
    watch_thread.start()

    update_status()


def stop_hosting():
    global httpd, watching
    watching = False
    if httpd:
        httpd.shutdown()
        httpd.server_close()
        httpd = None
    update_status()


def restart_server(directory):
    stop_hosting()
    time.sleep(1)
    start_hosting()


# -------------------------
# GUI Functions
# -------------------------
def browse_directory():
    selected = filedialog.askdirectory()
    if selected:
        dir_path.set(selected)


def update_status():
    if is_port_in_use(PORT):
        pid = get_pid_using_port(PORT)
        status_label.config(
            text=f"Port {PORT} ACTIVE (PID: {pid})",
            fg="red"
        )
        force_btn.config(state="normal")
    else:
        status_label.config(
            text=f"Port {PORT} FREE",
            fg="green"
        )
        force_btn.config(state="disabled")


def force_stop():
    pid = get_pid_using_port(PORT)
    if pid:
        if force_kill_process(pid):
            messagebox.showinfo("Success", "Process killed.")
        else:
            messagebox.showerror("Error", "Could not kill process.")
    update_status()

# -------------------------
# Open the localhost with browser
# -------------------------

def open_browser():
    webbrowser.open(f"http://localhost:{PORT}")


# -------------------------
# GUI Setup
# -------------------------
root = tk.Tk()
root.title(f"Localhost:{PORT} Manager")
root.geometry("600x350")

# Create a frame to hold the directory selection widgets side-by-side
dir_frame = tk.Frame(root)
dir_frame.pack(pady=20, padx=10, fill="x")

dir_path = tk.StringVar(value=os.getcwd())

tk.Label(dir_frame, text="Directory to Host:").pack(side=tk.LEFT, padx=5)
tk.Entry(dir_frame, textvariable=dir_path, width=55).pack(side=tk.LEFT, padx=5, expand=True, fill='x')
tk.Button(dir_frame, text="Browse", command=browse_directory).pack(side=tk.LEFT, padx=5)

status_label = tk.Label(root, text="")
status_label.pack(pady=2)
tk.Button(root, text="Refresh Status", command=update_status).pack(pady=(0,8))

tk.Button(root, text="Start Hosting", command=start_hosting, bg="lightgreen").pack(pady=5)
tk.Button(root, text="Stop Hosting", command=stop_hosting, bg="orange").pack(pady=5)

force_btn = tk.Button(root, text="Force Stop Port Process", command=force_stop, bg="red")
force_btn.pack(pady=20)


tk.Button(root, text="Open in Browser", command=open_browser).pack()


update_status()

root.mainloop()