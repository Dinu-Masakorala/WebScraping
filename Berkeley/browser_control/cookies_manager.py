import os
import json

# Path to save the cookies file
COOKIES_FILE = os.path.join(os.getcwd(), "cookies.json")

def save_cookies(driver):
    """Save cookies to a file."""
    cookies = driver.get_cookies()
    with open(COOKIES_FILE, 'w') as file:
        json.dump(cookies, file)
    print(f"✅ Cookies saved to {COOKIES_FILE}")

def load_cookies(driver):
    """Load cookies from a file."""
    if not os.path.exists(COOKIES_FILE):
        print("⚠️ No cookies file found. Skipping cookie loading.")
        return

    with open(COOKIES_FILE, 'r') as file:
        cookies = json.load(file)

    driver.delete_all_cookies()
    for cookie in cookies:
        # Fix domain if necessary
        if 'sameSite' in cookie and cookie['sameSite'] == 'None':
            cookie['sameSite'] = 'Strict'
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(f"⚠️ Could not add cookie: {e}")
    print("✅ Cookies loaded.")

