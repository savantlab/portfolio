#!/usr/bin/env python3
"""
Generate PDF from resume markdown file
Usage: python generate_resume_pdf.py
"""
import markdown
import subprocess
import os

# Read markdown file
with open('palantir_echo_resume_pitch.md', 'r') as f:
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
with open('temp_resume.html', 'w') as f:
    f.write(styled_html)

print("HTML generated: temp_resume.html")
print("\nTo generate PDF, run one of:")
print("  1. Open temp_resume.html in browser and print to PDF")
print("  2. Install wkhtmltopdf: brew install wkhtmltopdf")
print("     Then run: wkhtmltopdf temp_resume.html stephanie_king_resume.pdf")
print("  3. Install weasyprint: pip install weasyprint")
print("     Then run: weasyprint temp_resume.html stephanie_king_resume.pdf")
