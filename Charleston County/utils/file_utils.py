import os
import base64
from config import BASE_OUTPUT_DIR

def create_output_directory(tms_number):
    """Create output directory for a TMS number"""
    folder_path = os.path.join(BASE_OUTPUT_DIR, tms_number)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def save_pdf(driver, file_path):
    """Save current page as PDF"""
    pdf_data = driver.execute_cdp_cmd("Page.printToPDF", {
        "landscape": False,
        "printBackground": True
    })
    with open(file_path, 'wb') as f:
        f.write(base64.b64decode(pdf_data['data']))