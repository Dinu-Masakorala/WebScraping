def solve_captcha_if_present(driver):
    """Pause execution to allow user to solve CAPTCHA manually."""
    print("⚠️  If CAPTCHA is present, solve it in the browser window.")
    input("✅ Press ENTER here AFTER solving the CAPTCHA...")
