#!/usr/bin/env python3
"""
Flask + Chromedriver Lifecycle Manager

Runs a Flask application and automatically manages Chrome/Chromedriver lifecycle.
The app shuts down when the browser window is closed.

Usage:
    python flask_driver_runner.py app:app [--headless] [--port PORT] [--host HOST]
"""

import sys
import argparse
import threading
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import importlib


def get_chrome_driver(headless=False):
    """
    Create and configure a Chrome WebDriver instance.
    
    Args:
        headless (bool): Run Chrome in headless mode (no visible window)
    
    Returns:
        webdriver.Chrome: Configured Chrome driver instance
    """
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument('--headless')
    
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except WebDriverException as e:
        print(f"Error creating Chrome driver: {e}")
        print("\nMake sure you have Chrome installed.")
        sys.exit(1)


def monitor_driver(driver, app_thread):
    """
    Monitor the Chrome driver and shutdown when it closes.
    
    Args:
        driver: Selenium WebDriver instance
        app_thread: Thread running the Flask app
    """
    try:
        while True:
            try:
                # Check if driver is still alive by getting current URL
                _ = driver.current_url
                time.sleep(1)
            except WebDriverException:
                # Driver closed, shutdown the app
                print("\n[DRIVER MONITOR] Browser closed, shutting down Flask app...")
                # Force exit since Flask doesn't have a clean shutdown mechanism in dev mode
                import os
                os._exit(0)
    except KeyboardInterrupt:
        print("\n[DRIVER MONITOR] Received interrupt, shutting down...")
        driver.quit()
        sys.exit(0)


def run_app_with_driver(app, host='127.0.0.1', port=5001, headless=False):
    """
    Run a Flask app with Chrome driver lifecycle management.
    
    Args:
        app: Flask application instance
        host (str): Host to bind Flask server
        port (int): Port to bind Flask server
        headless (bool): Run Chrome in headless mode
    
    Returns:
        webdriver.Chrome: Driver instance (for programmatic use)
    """
    # Start Flask in a separate thread
    def run_flask():
        app.run(host=host, port=port, debug=False, use_reloader=False)
    
    app_thread = threading.Thread(target=run_flask, daemon=True)
    app_thread.start()
    
    # Give Flask time to start
    print(f"[FLASK] Starting Flask app on {host}:{port}...")
    time.sleep(2)
    
    # Create and configure driver
    print(f"[DRIVER] Starting Chrome driver (headless={headless})...")
    driver = get_chrome_driver(headless=headless)
    
    # Navigate to the Flask app
    url = f"http://{host}:{port}"
    print(f"[DRIVER] Opening {url}...")
    driver.get(url)
    
    # Start monitoring thread
    monitor_thread = threading.Thread(target=monitor_driver, args=(driver, app_thread), daemon=True)
    monitor_thread.start()
    
    print("[READY] Flask app is running with Chrome driver.")
    print("       Close the browser window to shutdown the app.")
    print("       Or press Ctrl+C to exit.\n")
    
    return driver


def main():
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(description='Run Flask app with Chrome driver lifecycle management')
    parser.add_argument('app_module', help='Flask app module in format "module:app"')
    parser.add_argument('--headless', action='store_true', help='Run Chrome in headless mode')
    parser.add_argument('--port', type=int, default=5001, help='Port for Flask server (default: 5001)')
    parser.add_argument('--host', default='127.0.0.1', help='Host for Flask server (default: 127.0.0.1)')
    
    args = parser.parse_args()
    
    # Parse module and app name
    try:
        module_name, app_name = args.app_module.split(':')
    except ValueError:
        print("Error: app_module must be in format 'module:app'")
        print("Example: python flask_driver_runner.py app:app")
        sys.exit(1)
    
    # Import the Flask app
    try:
        module = importlib.import_module(module_name)
        app = getattr(module, app_name)
    except (ImportError, AttributeError) as e:
        print(f"Error loading Flask app: {e}")
        sys.exit(1)
    
    # Run the app with driver
    driver = run_app_with_driver(app, host=args.host, port=args.port, headless=args.headless)
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[MAIN] Shutting down...")
        driver.quit()
        sys.exit(0)


if __name__ == '__main__':
    main()
