# TheStatPy HTML Tag Processing

## Overview

This implementation adds support for processing `<thestatpy>` custom HTML tags that are used for modular HTML composition. When the `<import app="thestatpy"/>` declaration is present in an HTML file, the build system will automatically replace `<thestatpy html="path/to/file.html">` tags with the actual content from the referenced files.

## Features

✅ **Automatic tag replacement** - Replaces `<thestatpy>` tags with external HTML content  
✅ **Build integration** - Seamlessly integrated into the existing build pipeline  
✅ **Standalone utility** - Can be used independently without the build system  
✅ **Error handling** - Gracefully handles missing files and processing errors  
✅ **BeautifulSoup-powered** - Uses industry-standard HTML parsing

## Files Modified

### 1. **build.py**
   - Added `process_thestatpy()` function to parse and replace tags
   - Updated `process_file()` to call thestatpy processing before minification for HTML files
   - Updated dependency loading to include BeautifulSoup4

### 2. **requirements-build.txt**
   - Added `beautifulsoup4` as a build dependency

### 3. **process_thestatpy.py** (NEW)
   - Standalone script for processing thestatpy tags
   - Can be used independently or within the build pipeline
   - Includes verbose mode for debugging

## How It Works

### Basic Usage

**Source HTML (src/index.html):**
```html
<!DOCTYPE html>
<html>
<head>
    <!-- Declare thestatpy tag handling -->
    <import app="thestatpy"/>
</head>
<body>
    <!-- Reference external HTML file -->
    <thestatpy html="part/edit-modal.html"></thestatpy>
    <thestatpy html="part/about-modal.html"></thestatpy>
</body>
</html>
```

**External file content (src/part/edit-modal.html):**
```html
<div id="editModal" class="modal hidden">
    <div class="modal-content">
        <!-- Modal content here -->
    </div>
</div>
```

**After processing:**
```html
<!DOCTYPE html>
<html>
<head>
    <!-- Import tag remains unchanged -->
    <import app="thestatpy"/>
</head>
<body>
    <!-- Thestatpy tags are replaced with actual content -->
    <div id="editModal" class="modal hidden">
        <div class="modal-content">
            <!-- Modal content here -->
        </div>
    </div>
    
    <div id="aboutModal" class="modal hidden">
        <!-- About modal content -->
    </div>
</body>
</html>
```

## Usage

### Option 1: Via Build System

Run the build process as usual. TheStatPy processing happens automatically for HTML files:

```bash
python build.py
```

The build process will:
1. Detect `<import app="thestatpy"/>` in HTML files
2. Find all `<thestatpy html="...">` tags
3. Load content from referenced files
4. Replace tags with actual content
5. Minify the result

### Option 2: Standalone Script

Use the standalone utility directly:

```bash
# Process and output to stdout
python process_thestatpy.py src/index.html

# Process and save to file
python process_thestatpy.py src/index.html output.html

# Verbose output for debugging
python process_thestatpy.py -v src/index.html

# Get help
python process_thestatpy.py --help
```

## Processing Order

For HTML files processed through build.py:

```
1. Read HTML file
2. Process <thestatpy> tags (replace with external content)
3. Minify the result
4. Write to build directory
```

This ensures:
- External files are properly inlined before minification
- The minification process compresses the final output efficiently
- No duplicate processing or nested thestatpy issues

## Requirements

- **Python 3.6+**
- **beautifulsoup4** - HTML parsing library

Install dependencies:
```bash
pip install -r requirements-build.txt
```

Or install individually:
```bash
pip install beautifulsoup4
```

## Benefits

1. **Modular HTML** - Keep modal and component HTML in separate files
2. **Build-time optimization** - Components are inlined before passing to minifier
3. **Better organization** - Logical file structure without runtime parsing overhead
4. **Performance** - No JavaScript runtime processing needed
5. **Flexibility** - Works with any build system, also available as standalone tool

## Example Workflow

```bash
# Development: Use standalone script to preview changes
python process_thestatpy.py -v src/index.html

# Production: Run full build with all optimizations
python build.py
```

## Error Handling

The processor gracefully handles:

- **Missing files** - Warns and skips missing HTML files
- **Missing import tag** - Returns original content unchanged
- **No thestatpy tags** - Returns original content unchanged
- **Invalid paths** - Provides helpful error messages in verbose mode

## Testing

Verify the implementation:

```bash
# Test with verbose output
python process_thestatpy.py -v src/index.html

# Expected output:
# ✓ Found <import app='thestatpy'/> tag
# ✓ Found 2 <thestatpy> tag(s)
#   ✓ Replaced <thestatpy html='part/edit-modal.html'>
#   ✓ Replaced <thestatpy html='part/about-modal.html'>
# Processing complete: 2/2 tags replaced
```

## Technical Details

### File Path Resolution

Relative paths in `html` attributes are resolved relative to the directory containing the source HTML file:

```
Source: src/index.html
Path:   part/edit-modal.html
Resolves to: src/part/edit-modal.html
```

### BeautifulSoup Parser

Uses the default HTML parser from BeautifulSoup for compatibility and speed.

### Integration with Minification

TheStatPy processing occurs **before** minification, ensuring:
- All external content is properly inlined
- Minifier can optimize the complete document
- No conflicts with minification settings
