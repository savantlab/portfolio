#!/usr/bin/env python3
"""
Setup script to download and configure chromedriver for development.
Automatically manages chromedriver version matching your Chrome browser.
"""

import os
import sys
from webdriver_manager.chrome import ChromeDriverManager

def setup_chromedriver():
    """Download and setup chromedriver for development."""
    try:
        print("Setting up chromedriver...")
        
        # Use webdriver-manager to automatically download the correct version
        driver_path = ChromeDriverManager().install()
        
        print(f"✓ Chromedriver installed at: {driver_path}")
        
        # Create a convenience module for importing chromedriver
        module_content = f'''"""Auto-configured chromedriver module."""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_chrome_driver(headless=False):
    """Get a configured Chrome webdriver instance.
    
    Args:
        headless: Run Chrome in headless mode (no UI)
    
    Returns:
        selenium.webdriver.Chrome: Configured Chrome webdriver
    """
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

__all__ = ["get_chrome_driver"]
'''
        
        with open("chromedriver_config.py", "w") as f:
            f.write(module_content)
        
        print("✓ Created chromedriver_config.py module")
        print("\nUsage in your code:")
        print("  from chromedriver_config import get_chrome_driver")
        print("  driver = get_chrome_driver()")
        
        return True
        
    except Exception as e:
        print(f"✗ Error setting up chromedriver: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    success = setup_chromedriver()
    sys.exit(0 if success else 1)
