from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # Add this import

def extract_deed_info(driver, wait, tms_number):
    """Extract deed book and page numbers from property page"""
    book_numbers = []
    page_numbers = []
    table_xpath = '/html/body/form/div[3]/div[5]/main/div/div[1]/div/div[4]/div/div/div/table'
    
    try:
        table_element = wait.until(EC.presence_of_element_located((By.XPATH, table_xpath)))
        table_body = table_element.find_element(By.TAG_NAME, 'tbody')
        rows = table_body.find_elements(By.TAG_NAME, 'tr')

        for row in rows:
            try:
                td_elements = row.find_elements(By.TAG_NAME, 'td')
                if len(td_elements) >= 2:
                    book = td_elements[0].text.strip()
                    page = td_elements[1].text.strip()

                    if book and page:
                        if book.isdigit():
                            book = book.zfill(4)
                        page = page.zfill(3)
                        book_numbers.append(book)
                        page_numbers.append(page)
            except StaleElementReferenceException:
                print("♻️ Stale element encountered in row - continuing")
                continue

        print(f"✅ Extracted {len(book_numbers)} deed records for {tms_number}")
        return book_numbers, page_numbers
        
    except Exception as e:
        print(f"❌ Failed to extract deed info for {tms_number}: {e}")
        return [], []  # Return empty lists to allow continuation