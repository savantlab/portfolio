#!/usr/bin/env python3
"""
Flask + Chromedriver lifecycle manager.

Runs a Flask app and chromedriver in tandem, shutting down the app
when the driver closes. Useful for integration testing and automation.

Usage:
    python -m flask_driver_runner app:app --driver-headless
    python -m flask_driver_runner app:app --port 5001
"""

import argparse
import atexit
import sys
import threading
import time
from functools import wraps
from typing import Optional

from flask import Flask
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class FlaskDriverRunner:
    """Manages Flask app and chromedriver as a single lifecycle."""

    def __init__(self, app: Flask, headless: bool = False, port: int = 5001, host: str = "127.0.0.1"):
        """
        Initialize Flask + Driver runner.

        Args:
            app: Flask application instance
            headless: Run Chrome in headless mode
            port: Port for Flask app
            host: Host for Flask app
        """
        self.app = app
        self.headless = headless
        self.port = port
        self.host = host
        self.driver = None
        self.flask_thread = None
        self.shutdown_event = threading.Event()

    def setup_driver(self) -> webdriver.Chrome:
        """Create and return configured Chrome webdriver."""
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument(f"--app={self.app.name}")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def run_flask(self):
        """Run Flask app in background thread."""
        self.app.run(
            host=self.host,
            port=self.port,
            debug=False,
            use_reloader=False,
            threaded=True,
        )

    def start(self) -> webdriver.Chrome:
        """
        Start Flask app and chromedriver together.

        Returns:
            selenium.webdriver.Chrome: The configured webdriver instance
        """
        # Start Flask in background thread
        self.flask_thread = threading.Thread(target=self.run_flask, daemon=True)
        self.flask_thread.start()

        # Give Flask time to start
        time.sleep(1)

        # Initialize driver
        self.driver = self.setup_driver()

        # Navigate to the app
        app_url = f"http://{self.host}:{self.port}"
        self.driver.get(app_url)

        # Setup shutdown hook
        atexit.register(self.shutdown)

        # Monitor driver for closure
        self._monitor_driver()

        return self.driver

    def _monitor_driver(self):
        """Monitor driver and shutdown app if driver closes."""

        def check_driver():
            """Check if driver is still alive."""
            while not self.shutdown_event.is_set():
                try:
                    # Simple check - if this fails, driver is closed
                    _ = self.driver.window_handles
                    time.sleep(0.5)
                except Exception:
                    # Driver closed, shutdown everything
                    print("\n✓ Driver closed, shutting down Flask app...")
                    self.shutdown()
                    sys.exit(0)

        monitor_thread = threading.Thread(target=check_driver, daemon=True)
        monitor_thread.start()

    def shutdown(self):
        """Shutdown driver and signal Flask to stop."""
        self.shutdown_event.set()

        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass

        print("✓ Flask + Driver shutdown complete")


def run_app_with_driver(
    app: Flask, headless: bool = False, port: int = 5001, host: str = "127.0.0.1"
) -> webdriver.Chrome:
    """
    Convenience function to run Flask app with chromedriver.

    Args:
        app: Flask application instance
        headless: Run Chrome in headless mode
        port: Port for Flask app
        host: Host for Flask app

    Returns:
        selenium.webdriver.Chrome: The configured webdriver instance

    Example:
        from flask import Flask
        from flask_driver_runner import run_app_with_driver

        app = Flask(__name__)

        @app.route("/")
        def hello():
            return "Hello World"

        if __name__ == "__main__":
            driver = run_app_with_driver(app, headless=True)
            driver.get(f"http://localhost:5001")
            # App shuts down when driver closes
    """
    runner = FlaskDriverRunner(app, headless=headless, port=port, host=host)
    return runner.start()


def main():
    """CLI entry point for running Flask apps with chromedriver."""
    parser = argparse.ArgumentParser(
        description="Run Flask app with chromedriver lifecycle management"
    )
    parser.add_argument(
        "app",
        help="Flask app reference (e.g., 'app:app' or 'mymodule:create_app()')",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5001,
        help="Port to run Flask app on (default: 5001)",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind Flask app to (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run Chrome in headless mode",
    )

    args = parser.parse_args()

    # Import the Flask app
    module_name, app_name = args.app.rsplit(":", 1)
    module = __import__(module_name, fromlist=[app_name])
    app = getattr(module, app_name)

    # Only call if it looks like a factory function (has callable with params)
    if callable(app) and not isinstance(app, Flask):
        try:
            app = app()
        except TypeError:
            pass  # Not a factory, it's the Flask instance itself

    print(f"Starting Flask app on {args.host}:{args.port}...")
    print(f"Chrome driver: {'headless' if args.headless else 'visible'}")

    runner = FlaskDriverRunner(
        app, headless=args.headless, port=args.port, host=args.host
    )
    driver = runner.start()

    print(f"✓ Flask app running at http://{args.host}:{args.port}")
    print(f"✓ Chrome driver ready")
    print("Close the Chrome window to shutdown the Flask app.\n")

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        runner.shutdown()


if __name__ == "__main__":
    main()
