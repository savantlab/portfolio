"""Auto-configured chromedriver module."""
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
