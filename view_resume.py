#!/usr/bin/env python3
"""
Keep resume PDF open in browser using Selenium
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup Chrome driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Navigate to the resume
url = "https://savantlab.org/gorgon/resume.pdf?password=ARCHIMEDES2026"
driver.get(url)

print(f"✓ Opened resume in browser: {url}")
print("Browser will stay open. Press Ctrl+C to close.")

try:
    # Keep browser open indefinitely
    while True:
        time.sleep(60)
        # Optional: refresh every 5 minutes to keep connection alive
        # driver.refresh()
except KeyboardInterrupt:
    print("\nClosing browser...")
    driver.quit()
