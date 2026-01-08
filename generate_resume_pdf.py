#!/usr/bin/env python3
"""
Generate PDF from resume markdown file
Usage: python generate_resume_pdf.py
"""
import markdown
import subprocess
import os
import sys

# Check if weasyprint is available
try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

# Read markdown file
md_file = 'resume.md'
if not os.path.exists(md_file):
    print(f"Error: {md_file} not found")
    sys.exit(1)

with open(md_file, 'r') as f:
    md_content = f.read()

# Convert to HTML with styling
html_content = markdown.markdown(md_content, extensions=['fenced_code', 'tables', 'toc'])

# Add CSS styling for professional resume look
styled_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page {{
            size: letter;
            margin: 0.75in;
        }}
        body {{
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
            max-width: 8.5in;
            margin: 0 auto;
        }}
        h1 {{
            font-size: 28pt;
            font-weight: 700;
            margin-bottom: 8px;
            color: #000;
            border-bottom: 3px solid #2c5aa0;
            padding-bottom: 8px;
        }}
        h2 {{
            font-size: 18pt;
            font-weight: 600;
            margin-top: 24px;
            margin-bottom: 12px;
            color: #2c5aa0;
        }}
        h3 {{
            font-size: 14pt;
            font-weight: 600;
            margin-top: 16px;
            margin-bottom: 8px;
            color: #444;
        }}
        p {{
            margin-bottom: 8px;
        }}
        ul, ol {{
            margin-bottom: 12px;
            padding-left: 24px;
        }}
        li {{
            margin-bottom: 4px;
        }}
        code {{
            background: #f5f5f5;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 10pt;
        }}
        pre {{
            background: #f5f5f5;
            padding: 12px;
            border-radius: 4px;
            overflow-x: auto;
            font-size: 9pt;
        }}
        strong {{
            font-weight: 600;
            color: #000;
        }}
        hr {{
            border: none;
            border-top: 2px solid #ddd;
            margin: 16px 0;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>
"""

# Save HTML temporarily
html_file = 'temp_resume.html'
pdf_file = 'resume.pdf'

with open(html_file, 'w') as f:
    f.write(styled_html)

print(f"✓ HTML generated: {html_file}")

# Try to generate PDF automatically
if WEASYPRINT_AVAILABLE:
    try:
        HTML(string=styled_html).write_pdf(pdf_file)
        print(f"✓ PDF generated: {pdf_file}")
        file_size = os.path.getsize(pdf_file) / 1024
        print(f"  Size: {file_size:.1f} KB")
    except Exception as e:
        print(f"Error generating PDF with weasyprint: {e}")
        print("\nFallback: Open temp_resume.html in browser and print to PDF")
else:
    print("\nTo generate PDF automatically, install weasyprint:")
    print("  pip install weasyprint")
    print("\nOr generate manually:")
    print(f"  1. Open {html_file} in browser and print to PDF")
    print(f"  2. Install wkhtmltopdf: brew install wkhtmltopdf")
    print(f"     Then run: wkhtmltopdf {html_file} {pdf_file}")
