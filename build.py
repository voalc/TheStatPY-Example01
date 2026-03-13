import os
import re
import shutil

SRC_DIR = "./src"
BUILD_DIR = "./build"


def ensure_build_dir():
    os.makedirs(BUILD_DIR, exist_ok=True)


def sync_build_dir():
    """Remove files/folders from build that don't exist in src."""
    if not os.path.exists(BUILD_DIR):
        return
    
    # Collect all relative paths that should exist in build
    src_items = set()
    for root, dirs, files in os.walk(SRC_DIR):
        rel_dir = os.path.relpath(root, SRC_DIR)
        if rel_dir != '.':
            src_items.add(rel_dir)
        for file in files:
            src_rel_path = os.path.relpath(os.path.join(root, file), SRC_DIR)
            src_items.add(src_rel_path)
    
    # Remove files/folders from build that don't exist in src (process bottom-up)
    for root, dirs, files in os.walk(BUILD_DIR, topdown=False):
        for file in files:
            build_file = os.path.join(root, file)
            rel_path = os.path.relpath(build_file, BUILD_DIR)
            if rel_path not in src_items:
                os.remove(build_file)
        
        for dir_name in dirs:
            build_dir = os.path.join(root, dir_name)
            rel_path = os.path.relpath(build_dir, BUILD_DIR)
            if rel_path not in src_items:
                shutil.rmtree(build_dir)


def minify_html(content):
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    content = re.sub(r'>\s+<', '><', content)
    content = re.sub(r'\s+', ' ', content)
    return content.strip()


def minify_css(content):
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    content = re.sub(r'\s+', ' ', content)
    content = re.sub(r'\s*([{}:;,])\s*', r'\1', content)
    content = re.sub(r';}', '}', content)
    return content.strip()


def minify_js(content):
    content = re.sub(r'//.*', '', content)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    content = re.sub(r'\s+', ' ', content)
    content = re.sub(r'\s*([{}();,:+\-*/=<>])\s*', r'\1', content)
    return content.strip()


def process_file(src_path, dest_path):
    ext = os.path.splitext(src_path)[1].lower()

    if ext in [".html", ".css", ".js"]:
        with open(src_path, "r", encoding="utf-8") as f:
            content = f.read()

        if ext == ".html":
            content = minify_html(content)
        elif ext == ".css":
            content = minify_css(content)
        elif ext == ".js":
            content = minify_js(content)

        with open(dest_path, "w", encoding="utf-8") as f:
            f.write(content)
    else:
        shutil.copy2(src_path, dest_path)


def build():
    ensure_build_dir()
    sync_build_dir()

    for root, dirs, files in os.walk(SRC_DIR):
        rel_path = os.path.relpath(root, SRC_DIR)
        build_root = os.path.join(BUILD_DIR, rel_path)

        os.makedirs(build_root, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(build_root, file)
            process_file(src_file, dest_file)

    print("Build completed successfully.")


if __name__ == "__main__":
    build()