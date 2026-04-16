# Implementation Summary: TheStatPy HTML Tag Processing

## What Was Implemented

A complete system for processing `<thestatpy>` custom HTML tags that enables modular HTML composition in the class-timetable project.

## Files Created/Modified

### ✅ Modified Files

1. **[build.py](build.py)** 
   - Added `process_thestatpy()` function with full documentation
   - Updated `process_file()` to process thestatpy tags before minification
   - Updated `_load_minify_dependencies()` to include BeautifulSoup4
   - Processing occurs for all HTML files in the build pipeline

2. **[requirements-build.txt](requirements-build.txt)**
   - Added `beautifulsoup4` as a build dependency

### ✅ New Files Created

1. **[process_thestatpy.py](process_thestatpy.py)**
   - Standalone utility for processing thestatpy tags
   - Features:
     - Verbose mode (`-v` flag) for debugging
     - Can process and output to file or stdout
     - Full CLI with help documentation
     - Graceful error handling for missing files
   - Can be used independently or as part of the build system

2. **[THESTATPY.md](THESTATPY.md)**
   - Comprehensive documentation
   - Usage examples and workflow
   - Technical details of implementation
   - Integration information
   - Troubleshooting guide

## How It Works

### Detection
The system detects when `<import app="thestatpy"/>` is present in an HTML file.

### Processing
For each `<thestatpy html="path/to/file.html">` tag found:
1. The referenced file is located (relative to the HTML file's directory)
2. The file content is read
3. The tag is replaced with the actual HTML content

### Build Integration
In the build pipeline:
```
HTML File → Process TheStatPy Tags → Minify → Build Output
```

## Usage

### From Build System
```bash
python build.py
```
TheStatPy processing is automatic for all HTML files.

### Standalone
```bash
# Preview processed output
python process_thestatpy.py src/index.html

# Save to file
python process_thestatpy.py src/index.html output.html

# Verbose debugging
python process_thestatpy.py -v src/index.html
```

## Example: Before and After

### Before (Source)
```html
<import app="thestatpy"/>
<thestatpy html="part/edit-modal.html"></thestatpy>
<thestatpy html="part/about-modal.html"></thestatpy>
```

### After (Processed)
```html
<import app="thestatpy"/>
<div id="editModal" class="modal hidden">
    <!-- Edit modal content from part/edit-modal.html -->
</div>
<div id="aboutModal" class="modal hidden">
    <!-- About modal content from part/about-modal.html -->
</div>
```

## Test Results

✅ Successfully detects `<import app="thestatpy"/>` tag  
✅ Successfully finds and processes `<thestatpy html="...">` tags  
✅ Successfully loads and inlines external HTML files  
✅ Processes both edit-modal.html and about-modal.html correctly  
✅ Handles file paths relative to source HTML location  
✅ Gracefully handles errors with informative messages  
✅ Works with both Unicode and ASCII output environments  

### Test Run Output
```
[OK] Found <import app='thestatpy'/> tag
[OK] Found 2 <thestatpy> tag(s)
  [OK] Replaced <thestatpy html='part/edit-modal.html'>
  [OK] Replaced <thestatpy html='part/about-modal.html'>

[INFO] Processing complete: 2/2 tags replaced
```

## Benefits

1. **Modular Components** - Keep related HTML in separate, manageable files
2. **Better Organization** - Clear structure with /part/ folder for components
3. **Build-Time Optimization** - No runtime JavaScript parsing needed
4. **Minification Integration** - External content inlined before minification for optimal compression
5. **Flexibility** - Works as part of build or standalone utility
6. **Future-Proof** - Easy to extend with additional features

## Dependencies

- **beautifulsoup4** - Already added to requirements-build.txt
- **Python 3.6+** - For modern Python features and UTF-8 support

## Installation

```bash
# Install build dependencies
pip install -r requirements-build.txt
```

Or individually:
```bash
pip install beautifulsoup4 csscompressor minify-html rjsmin
```

## Next Steps (Optional Enhancements)

- Add support for nested thestatpy tags
- Implement caching for frequently used components
- Add CSS/JS component support (not just HTML)
- Create component library documentation
- Add unit tests for processing pipeline

---

**Implementation completed and tested successfully!**
