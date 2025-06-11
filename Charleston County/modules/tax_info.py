import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.file_utils import save_pdf

def download_tax_info(driver, wait, folder_path):
    """Download tax information for a property"""
    try:
        print("➡️ Attempting to download tax info...")
        
        # Click the "Tax Info" link
        tax_info_link = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/form/div[3]/div[5]/main/div/div[1]/div/div[5]/div/div/div/div/div/div/div[3]/a/div/span')
        ))
        tax_info_link.click()
        time.sleep(3)  # Allow page to load

        # Remove nav/footer for clean PDF
        driver.execute_script("""
        var nav = document.querySelector('nav');
        if (nav) { nav.style.display = 'none'; }
        var footer = document.querySelector('footer');
        if (footer) { footer.style.display = 'none'; }
        """)

        # Save tax info PDF
        tax_info_pdf_path = os.path.join(folder_path, "Tax Info.pdf")
        save_pdf(driver, tax_info_pdf_path)
        print(f"✅ Successfully saved Tax Info PDF")
        
    except Exception as e:
        print(f"❌ Tax Info download failed: {str(e)}")
        raise  # Re-raise if you want main process to know it failed