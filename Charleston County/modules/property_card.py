import os  # Add this import at the top
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from utils.file_utils import create_output_directory, save_pdf
from config import PROPERTY_SEARCH_URL

def download_property_card(driver, wait, tms_number):
    """Download property card for a given TMS number"""
    try:
        driver.get(PROPERTY_SEARCH_URL)
        
        # Search by TMS number
        pin_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[title="PIN"]')))
        pin_input.clear()
        pin_input.send_keys(tms_number)
        pin_input.send_keys(Keys.RETURN)

        # Click view button
        view_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[3]/div[5]/main/div/div[1]/div/div[3]/div/div/div/tr-quick-search-root/div/tr-container-component/div/ngb-tabset/div/div/div/div/tr-search-result-component/div[2]/div[2]/div[1]/a')))
        view_button.click()

        # Create directory and save PDF
        folder_path = create_output_directory(tms_number)
        pdf_path = os.path.join(folder_path, "Property Card.pdf")
        save_pdf(driver, pdf_path)
        
        print(f"✅ Property Card PDF saved for {tms_number}")
        return folder_path
        
    except Exception as e:
        print(f"❌ Failed to download property card for {tms_number}: {e}")
        raise