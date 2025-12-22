#!/usr/bin/env python3
"""
Simple Markdown Viewer using Selenium
Opens markdown files rendered as HTML in your browser
"""
import sys
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import markdown

def render_markdown(md_file):
    """Convert markdown file to HTML with styling"""
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(md_content, extensions=['fenced_code', 'tables', 'codehilite'])
    
    # Create full HTML page with GitHub-like styling
    html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{os.path.basename(md_file)}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #24292e;
            max-width: 900px;
            margin: 40px auto;
            padding: 0 20px;
            background-color: #ffffff;
        }}
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
            line-height: 1.25;
        }}
        h1 {{ font-size: 2em; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }}
        h2 {{ font-size: 1.5em; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }}
        h3 {{ font-size: 1.25em; }}
        code {{
            background-color: #f6f8fa;
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
            font-size: 85%;
        }}
        pre {{
            background-color: #f6f8fa;
            padding: 16px;
            overflow: auto;
            border-radius: 6px;
            line-height: 1.45;
        }}
        pre code {{
            background-color: transparent;
            padding: 0;
        }}
        a {{
            color: #0366d6;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        blockquote {{
            padding: 0 1em;
            color: #6a737d;
            border-left: 0.25em solid #dfe2e5;
            margin: 0;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 16px 0;
        }}
        table th, table td {{
            padding: 6px 13px;
            border: 1px solid #dfe2e5;
        }}
        table tr:nth-child(2n) {{
            background-color: #f6f8fa;
        }}
        img {{
            max-width: 100%;
        }}
        ul, ol {{
            padding-left: 2em;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>
"""
    return html_template

def open_in_browser(md_file):
    """Open markdown file in browser using Selenium"""
    if not os.path.exists(md_file):
        print(f"Error: File '{md_file}' not found")
        sys.exit(1)
    
    # Convert markdown to HTML
    html_content = render_markdown(md_file)
    
    # Create temporary HTML file
    temp_html = f"/tmp/{Path(md_file).stem}_rendered.html"
    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Open in browser using Selenium
    print(f"Opening {md_file} in browser...")
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(f"file://{temp_html}")
    
    print("Browser opened. Press Ctrl+C to close and exit.")
    try:
        # Keep the script running
        input()
    except KeyboardInterrupt:
        print("\nClosing browser...")
    finally:
        driver.quit()
        os.remove(temp_html)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python md_viewer.py <markdown_file.md>")
        sys.exit(1)
    
    md_file = sys.argv[1]
    open_in_browser(md_file)
