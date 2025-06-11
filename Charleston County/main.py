import os
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from utils.webdriver_utils import setup_driver, restart_driver
from modules.property_card import download_property_card
from modules.deed_info import extract_deed_info
from modules.tax_info import download_tax_info
from modules.document_download import process_deed_pdfs  # Updated to use process_deed_pdfs
from config import EXCEL_FILE, EXCEL_COLUMN, DRIVER_TIMEOUT

def load_tms_numbers():
    """Load TMS numbers from Excel file"""
    df = pd.read_excel(EXCEL_FILE)
    df[EXCEL_COLUMN] = df[EXCEL_COLUMN].apply(lambda x: str(int(x)) if pd.notna(x) else '')
    return df[EXCEL_COLUMN].tolist()

def process_tms_number(driver, wait, tms_number):
    """Process a single TMS number"""
    if not tms_number:
        return
        
    try:
        # Step 1: Download property card
        folder_path = download_property_card(driver, wait, tms_number)
        
        # Step 2: Extract deed info
        book_numbers, page_numbers = extract_deed_info(driver, wait, tms_number)
        
        # Step 3: Download tax info
        download_tax_info(driver, wait, folder_path)
        
        # Step 4: Download deed documents
        if book_numbers and page_numbers:
            process_deed_pdfs(driver, wait, book_numbers, page_numbers, folder_path)
            
        print(f"✅ Completed all PDFs for {tms_number}")
        
    except Exception as e:
        print(f"❌ Failed to process {tms_number}: {e}")

def main():
    """Main execution function"""
    tms_list = load_tms_numbers()
    driver = setup_driver()
    wait = WebDriverWait(driver, DRIVER_TIMEOUT)
    
    processed_count = 0
    
    for tms_number in tms_list:
        process_tms_number(driver, wait, tms_number)
        processed_count += 1
        
        # Restart driver periodically
        if processed_count % 10 == 0:
            driver = restart_driver(driver)
            wait = WebDriverWait(driver, DRIVER_TIMEOUT)
    
    driver.quit()

if __name__ == "__main__":
    main()
