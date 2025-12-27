#!/usr/bin/env python3
"""
Unified Development Environment Driver

Runs Jupyter, Flask, or both in a single Chrome/Chromedriver session.
The environment shuts down when the browser window is closed.

Usage:
    python unified_driver.py --flask app:app
    python unified_driver.py --jupyter
    python unified_driver.py --flask app:app --jupyter
    python unified_driver.py --flask app:app --jupyter --headless
    python unified_driver.py --flask app:app --port 5002 --jupyter-port 8889
"""

import sys
import argparse
import threading
import time
import subprocess
import os
import signal
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


def run_flask_server(app, host='127.0.0.1', port=5001):
    """Run Flask application in a background thread."""
    app.run(host=host, port=port, debug=False, use_reloader=False)


def run_jupyter_server(port=8888):
    """Run Jupyter notebook server in a subprocess."""
    cmd = ['jupyter', 'notebook', '--no-browser', f'--port={port}']
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def monitor_driver(driver, jupyter_process=None):
    """
    Monitor the Chrome driver and shutdown when it closes.
    
    Args:
        driver: Selenium WebDriver instance
        jupyter_process: Jupyter subprocess (if running)
    """
    try:
        while True:
            try:
                # Check if driver is still alive by getting current URL
                _ = driver.current_url
                time.sleep(1)
            except WebDriverException:
                # Driver closed, shutdown everything
                print("\n[DRIVER MONITOR] Browser closed, shutting down...")
                if jupyter_process:
                    print("[JUPYTER] Stopping Jupyter server...")
                    jupyter_process.terminate()
                    jupyter_process.wait(timeout=5)
                # Force exit
                os._exit(0)
    except KeyboardInterrupt:
        print("\n[DRIVER MONITOR] Received interrupt, shutting down...")
        driver.quit()
        if jupyter_process:
            jupyter_process.terminate()
            jupyter_process.wait(timeout=5)
        sys.exit(0)


def main():
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(
        description='Run Jupyter, Flask, or both with Chrome driver lifecycle management'
    )
    parser.add_argument('--flask', metavar='APP', help='Flask app module in format "module:app"')
    parser.add_argument('--jupyter', action='store_true', help='Start Jupyter notebook')
    parser.add_argument('--headless', action='store_true', help='Run Chrome in headless mode')
    parser.add_argument('--port', type=int, default=5001, help='Port for Flask server (default: 5001)')
    parser.add_argument('--host', default='127.0.0.1', help='Host for Flask server (default: 127.0.0.1)')
    parser.add_argument('--jupyter-port', type=int, default=8888, help='Port for Jupyter (default: 8888)')
    
    args = parser.parse_args()
    
    # Validate that at least one service is requested
    if not args.flask and not args.jupyter:
        parser.error("Must specify at least one of --flask or --jupyter")
    
    flask_thread = None
    jupyter_process = None
    flask_url = None
    jupyter_url = None
    
    # Start Flask if requested
    if args.flask:
        try:
            module_name, app_name = args.flask.split(':')
        except ValueError:
            print("Error: --flask must be in format 'module:app'")
            print("Example: python unified_driver.py --flask app:app")
            sys.exit(1)
        
        try:
            module = importlib.import_module(module_name)
            app = getattr(module, app_name)
        except (ImportError, AttributeError) as e:
            print(f"Error loading Flask app: {e}")
            sys.exit(1)
        
        print(f"[FLASK] Starting Flask app on {args.host}:{args.port}...")
        flask_thread = threading.Thread(
            target=run_flask_server, 
            args=(app, args.host, args.port),
            daemon=True
        )
        flask_thread.start()
        flask_url = f"http://{args.host}:{args.port}"
        time.sleep(2)  # Give Flask time to start
    
    # Start Jupyter if requested
    if args.jupyter:
        print(f"[JUPYTER] Starting Jupyter notebook on port {args.jupyter_port}...")
        jupyter_process = run_jupyter_server(args.jupyter_port)
        jupyter_url = f"http://localhost:{args.jupyter_port}"
        time.sleep(3)  # Give Jupyter time to start
    
    # Create and configure driver
    print(f"[DRIVER] Starting Chrome driver (headless={args.headless})...")
    driver = get_chrome_driver(headless=args.headless)
    
    # Open Flask in first tab if requested
    if flask_url:
        print(f"[DRIVER] Opening Flask at {flask_url}...")
        driver.get(flask_url)
    
    # Open Jupyter in new tab if requested
    if jupyter_url:
        print(f"[DRIVER] Opening Jupyter at {jupyter_url}...")
        if flask_url:
            # Open new tab if Flask is already open
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
        driver.get(jupyter_url)
    
    # Start monitoring thread
    monitor_thread = threading.Thread(
        target=monitor_driver, 
        args=(driver, jupyter_process), 
        daemon=True
    )
    monitor_thread.start()
    
    print("\n[READY] Development environment is running.")
    if flask_url:
        print(f"       Flask: {flask_url}")
    if jupyter_url:
        print(f"       Jupyter: {jupyter_url}")
    print("       Close the browser window to shutdown.")
    print("       Or press Ctrl+C to exit.\n")
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[MAIN] Shutting down...")
        driver.quit()
        if jupyter_process:
            jupyter_process.terminate()
            jupyter_process.wait(timeout=5)
        sys.exit(0)


if __name__ == '__main__':
    main()
