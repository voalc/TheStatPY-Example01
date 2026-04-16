from adminonly.cli_alyod_text import cl
import os
import shutil
import importlib

SRC_DIR = os.path.join(os.getcwd(),"src") # ./src
BUILD_DIR = os.path.join(os.getcwd(),"build") # ./build


def _load_minify_dependencies():
    try:
        css_compress = importlib.import_module("csscompressor").compress
        html_minify = importlib.import_module("minify_html").minify
        js_minify = importlib.import_module("rjsmin").jsmin
        bs4 = importlib.import_module("bs4")
        return css_compress, html_minify, js_minify, bs4
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Missing build dependency. Install with: pip install -r requirements-build.txt or ensure the environment is set up correctly."
        ) from exc


CSS_COMPRESS, HTML_MINIFY, JS_MINIFY, BS4 = _load_minify_dependencies()


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
    return HTML_MINIFY(
        content,
        minify_css=True,
        minify_js=True,
        keep_comments=False,
    )


def minify_css(content):
    return CSS_COMPRESS(content)


def minify_js(content):
    return JS_MINIFY(content)


def _resolve_thestatpy_tags(html_content, base_dir, cache, include_stack=None):
    """Recursively resolve <thestatpy html="..."> tags using a shared component cache."""
    if include_stack is None:
        include_stack = set()

    soup = BS4.BeautifulSoup(html_content, 'html.parser')
    thestatpy_tags = soup.find_all('thestatpy', {'html': True})

    for tag in thestatpy_tags:
        html_path = tag.get('html')
        if not isinstance(html_path, str) or not html_path:
            continue

        file_path = os.path.abspath(os.path.join(base_dir, html_path))

        if file_path in include_stack:
            cl.paint(f"Warning: Circular include detected for '{html_path}'", "yellow")
            continue

        try:
            if not os.path.exists(file_path):
                cl.paint(f"Warning: File not found for '{html_path}'", "yellow")
                continue

            if file_path in cache:
                resolved_content = cache[file_path]
            else:
                include_stack.add(file_path)
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()

                resolved_content = _resolve_thestatpy_tags(
                    file_content,
                    os.path.dirname(file_path),
                    cache,
                    include_stack=include_stack,
                )
                cache[file_path] = resolved_content
                include_stack.remove(file_path)

            tag.replace_with(BS4.BeautifulSoup(resolved_content, 'html.parser'))
        except Exception as e:
            include_stack.discard(file_path)
            cl.paint(f"Warning: Could not load {html_path}: {e}", "yellow")

    return str(soup)


def process_thestatpy(html_content, base_dir):
    """
    Process <thestatpy> tags with html attributes.
    If <import app="thestatpy"/> is present, replace all <thestatpy html="path">
    elements with the actual content from the referenced files.
    
    Args:
        html_content: HTML content as string
        base_dir: Base directory to resolve relative paths from
    
    Returns:
        Processed HTML content
    """
    soup = BS4.BeautifulSoup(html_content, 'html.parser')
    
    # Check if <import app="thestatpy"/> exists
    import_tag = soup.find('import', {'app': 'thestatpy'})
    if not import_tag:
        return html_content

    # Remove control tag from final output after detection.
    import_tag.decompose()
    html_without_import_tag = str(soup)
    
    # Resolve tags recursively and reuse processed component content from cache.
    return _resolve_thestatpy_tags(html_without_import_tag, base_dir, cache={})


def process_file(src_path, dest_path):
    ext = os.path.splitext(src_path)[1].lower()

    if ext in [".html", ".css", ".js"]:
        with open(src_path, "r", encoding="utf-8") as f:
            content = f.read()

        if ext == ".html":
            # Process thestatpy tags first
            base_dir = os.path.dirname(src_path)
            content = process_thestatpy(content, base_dir)
            # Then minify
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
    _log =[
        cl.paint("  Build Process Completed Successfully!  ","bold", "bg_cyan", 'black'),
        cl.paint(f"Source Directory: {SRC_DIR}", "cyan"),
        cl.paint(f"Build Directory: {BUILD_DIR}", "cyan"),
        cl.paint("All HTML, CSS, and JS files have been minified for the build directory.", "yellow"),
    ]
    cl.box(_log, width=100, color="cyan")


if __name__ == "__main__":
    build()