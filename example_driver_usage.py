#!/usr/bin/env python3
"""
Example: Using Flask app with chromedriver lifecycle management.

This example shows how to run tests or automation with the Flask app
that automatically shuts down when the driver closes.
"""

from flask_driver_runner import run_app_with_driver
from app import app
import time


def example_with_automation():
    """Example: Automate interactions with the Flask app."""
    print("Starting Flask app with chromedriver...")
    driver = run_app_with_driver(app, headless=True, port=5001)

    try:
        # Navigate to the app
        driver.get("http://localhost:5001")
        print(f"Page title: {driver.title}")

        # Get all project links
        projects = driver.find_elements("xpath", "//a[contains(@href, '/project/')]")
        print(f"Found {len(projects)} projects")

        # Simulate some interactions
        time.sleep(2)

        # Driver closes -> Flask app automatically shuts down
        print("Test complete, closing driver...")

    finally:
        driver.quit()  # Close the driver - Flask app will follow


def example_with_visible_browser():
    """Example: Debug with a visible Chrome window."""
    print("Starting Flask app with visible Chrome window...")
    driver = run_app_with_driver(app, headless=False, port=5001)

    try:
        driver.get("http://localhost:5001")
        print("App loaded, interact with Chrome window...")
        print("Close Chrome when done - Flask will shutdown automatically")

        # Keep the script running while you interact
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        try:
            driver.quit()
        except Exception:
            pass


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "visible":
        example_with_visible_browser()
    else:
        example_with_automation()
