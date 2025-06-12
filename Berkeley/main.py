import logging
from config import DOWNLOAD_DIR, EXCEL_PATH
from browser_control.driver_manager import launch_undetected_browser
from browser_control.cookies_manager import load_cookies, save_cookies
from scraper.wildfire_search import search_properties
from scraper.property_card import download_property_card
from scraper.tax_info import download_tax_info
from scraper.deed_extractor import extract_deed_info
from documents.download_manager import download_deed_pdf
from utils.helpers import create_folder, setup_logging
from utils.captchas import solve_captcha_if_present

def main():
    # Setup logging and folders
    setup_logging()
    create_folder(DOWNLOAD_DIR)

    logging.info("🚀 Launching undetected browser...")
    driver, wait = launch_undetected_browser()

    try:
        # Optional: Load cookies for session reuse (if you implemented cookies_manager.py)
        load_cookies(driver)

        # Start scraping flow → get list of properties from Excel
        property_list = search_properties(driver, EXCEL_PATH)

        for property_data in property_list:
            solve_captcha_if_present(driver)

            # Download Property Card → get Book/Page info
            property_card_result = download_property_card(driver, property_data)

            # Download tax info (if implemented)
            download_tax_info(driver, property_data)

            # Extract deed info → use property_card_result (contains Book/Page)
            deed_info = extract_deed_info(driver, property_card_result)

            # Download deed PDF using extracted Book/Page info
            download_deed_pdf(driver, deed_info, property_data)

        # Save cookies for future runs
        save_cookies(driver)

    except Exception as e:
        logging.exception(f"❗ ERROR encountered during process: {e}")

    finally:
        driver.quit()
        logging.info("✅ Browser closed. Program complete.")

if __name__ == "__main__":
    main()
