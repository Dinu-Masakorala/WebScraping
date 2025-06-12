import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait

def launch_undetected_browser(headless=False):
    options = uc.ChromeOptions()
    options.add_argument('--start-maximized')
    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')

    driver = uc.Chrome(options=options, use_subprocess=True)
    wait = WebDriverWait(driver, 20)
    return driver, wait
