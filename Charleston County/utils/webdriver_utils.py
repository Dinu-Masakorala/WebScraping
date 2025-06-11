from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import HEADLESS, DRIVER_TIMEOUT

def setup_driver():
    """Setup and return a Chrome WebDriver instance"""
    options = Options()
    if HEADLESS:
        options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    return driver

def restart_driver(driver):
    """Restart the WebDriver to avoid crashes"""
    driver.quit()
    return setup_driver()