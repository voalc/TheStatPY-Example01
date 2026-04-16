#!/usr/bin/env python3
"""
Standalone utility to process <thestatpy> tags in HTML files.
This script detects <import app="thestatpy"/> and replaces all 
<thestatpy html="path"> elements with actual file content.

Usage:
    python process_thestatpy.py [input_html] [output_html]
    
If no arguments provided, processes src/index.html and outputs to stdout.
"""

import os
import sys
import argparse

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: beautifulsoup4 is required. Install with: pip install beautifulsoup4")
    sys.exit(1)


def _resolve_thestatpy_tags(html_content, base_dir, cache, include_stack=None, verbose=False):
    """Recursively resolve <thestatpy html="..."> tags using a shared component cache."""
    if include_stack is None:
        include_stack = set()

    soup = BeautifulSoup(html_content, 'html.parser')
    thestatpy_tags = soup.find_all('thestatpy', {'html': True})

    for tag in thestatpy_tags:
        html_path = tag.get('html')
        if not isinstance(html_path, str) or not html_path:
            continue

        file_path = os.path.abspath(os.path.join(base_dir, html_path))

        if file_path in include_stack:
            if verbose:
                print(f"  [ERROR] Circular include detected: {html_path}")
            continue

        try:
            if not os.path.exists(file_path):
                if verbose:
                    print(f"  [ERROR] File not found: {file_path}")
                continue

            if file_path in cache:
                resolved_content = cache[file_path]
                if verbose:
                    print(f"  [OK] Cache hit for '{html_path}'")
            else:
                include_stack.add(file_path)
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()

                resolved_content = _resolve_thestatpy_tags(
                    file_content,
                    os.path.dirname(file_path),
                    cache,
                    include_stack=include_stack,
                    verbose=verbose,
                )
                cache[file_path] = resolved_content
                include_stack.remove(file_path)

                if verbose:
                    print(f"  [OK] Cached component '{html_path}'")

            tag.replace_with(BeautifulSoup(resolved_content, 'html.parser'))
            if verbose:
                print(f"  [OK] Replaced <thestatpy html='{html_path}'>")
        except Exception as e:
            include_stack.discard(file_path)
            if verbose:
                print(f"  [ERROR] Error loading {html_path}: {e}")

    return str(soup)


def process_thestatpy(html_content, base_dir, verbose=False):
    """
    Process <thestatpy> tags with html attributes.
    If <import app="thestatpy"/> is present, replace all <thestatpy html="path">
    elements with the actual content from the referenced files.
    
    Args:
        html_content: HTML content as string
        base_dir: Base directory to resolve relative paths from
        verbose: Print debug information
    
    Returns:
        Processed HTML content
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Check if <import app="thestatpy"/> exists
    import_tag = soup.find('import', {'app': 'thestatpy'})
    if not import_tag:
        if verbose:
            print("[INFO] <import app='thestatpy'/> not found in HTML")
        return html_content

    # Remove control tag from final output after detection.
    import_tag.decompose()
    html_without_import_tag = str(soup)
    
    if verbose:
        print("[OK] Found <import app='thestatpy'/> tag")
    
    # Find all thestatpy tags with html attribute
    thestatpy_tags = soup.find_all('thestatpy', {'html': True})
    
    if not thestatpy_tags:
        if verbose:
            print("[INFO] No <thestatpy html='...'> tags found")
        return html_without_import_tag
    
    if verbose:
        print(f"[OK] Found {len(thestatpy_tags)} <thestatpy> tag(s)")
    
    cache = {}
    processed_html = _resolve_thestatpy_tags(html_without_import_tag, base_dir, cache, verbose=verbose)
    
    if verbose:
        print(f"\n[INFO] Processing complete: {len(thestatpy_tags)} top-level tag(s) scanned")
        print(f"[INFO] Cached components: {len(cache)}")
    
    return processed_html


def main():
    parser = argparse.ArgumentParser(
        description='Process <thestatpy> tags in HTML files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python process_thestatpy.py src/index.html              # Output to stdout
  python process_thestatpy.py src/index.html out.html     # Save to file
  python process_thestatpy.py -v src/index.html           # Verbose output
        '''
    )
    
    parser.add_argument('input', nargs='?', default='src/index.html',
                        help='Input HTML file (default: src/index.html)')
    parser.add_argument('output', nargs='?', 
                        help='Output HTML file (default: stdout)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Print detailed processing information')
    
    args = parser.parse_args()
    
    # Read input file
    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    with open(args.input, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Process
    base_dir = os.path.dirname(os.path.abspath(args.input))
    processed_content = process_thestatpy(html_content, base_dir, verbose=args.verbose)
    
    # Output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(processed_content)
        print(f"[OK] Output saved to: {args.output}")
    else:
        print(processed_content)


if __name__ == '__main__':
    main()
