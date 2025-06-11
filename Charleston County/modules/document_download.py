import os
import base64
import time
import random
import requests
from config import DEED_SEARCH_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime

def take_screenshot(driver, step_name, folder_path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    errors_folder = os.path.join(folder_path, "errors")
    os.makedirs(errors_folder, exist_ok=True) 
    screenshot_path = os.path.join(errors_folder, f"error_{step_name}_{timestamp}.png")
    driver.save_screenshot(screenshot_path)
    return screenshot_path

def handle_captcha_if_present(driver, wait_time=5):
    try:
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'recaptcha')]"))
        )
        print("⚠️ CAPTCHA detected! Please solve it in the browser window...")
        input("👉 Press Enter **AFTER** you solve the CAPTCHA to continue...")
    except TimeoutException:
        pass

def process_deed_pdfs(driver, wait, book_numbers, page_numbers, folder_path):
    errors_folder = os.path.join(folder_path, "errors")
    deeds_folder = os.path.join(folder_path, "deeds")

    os.makedirs(errors_folder, exist_ok=True)
    os.makedirs(deeds_folder, exist_ok=True)

    for book, page in zip(book_numbers, page_numbers):
        try:
            print(f"\n📖 Processing Book: {book}, Page: {page}")

            # STEP 1: Load deed search page
            try:
                driver.get(DEED_SEARCH_URL)
                wait.until(EC.presence_of_element_located((By.ID, 'booknumber')))
                take_screenshot(driver, "page_loaded", folder_path)
            except Exception as e:
                take_screenshot(driver, "page_load_failed", folder_path)
                print(f"❌ Failed to load search page - {e}")
                continue

            # STEP 2: Enter search criteria
            try:
                book_input = wait.until(EC.presence_of_element_located((By.ID, 'booknumber')))
                book_input.clear()
                book_input.send_keys(book)

                page_input = wait.until(EC.presence_of_element_located((By.ID, 'pagenumber')))
                page_input.clear()
                page_input.send_keys(page)

                try:
                    legal_checkbox = driver.find_element(By.XPATH, '//*[@id="form"]/input[2]')
                    if not legal_checkbox.is_selected():
                        driver.execute_script("arguments[0].click();", legal_checkbox)
                except NoSuchElementException:
                    pass

                take_screenshot(driver, "search_criteria_entered", folder_path)
            except Exception as e:
                take_screenshot(driver, "search_entry_failed", folder_path)
                print(f"❌ Failed to enter search criteria - {e}")
                continue

            # STEP 3: Click Search
            try:
                search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'form#form input.submit')))
                driver.execute_script("arguments[0].click();", search_button)
                take_screenshot(driver, "search_clicked", folder_path)
            except Exception as e:
                take_screenshot(driver, "search_click_failed", folder_path)
                print(f"❌ Failed to click search - {e}")
                continue

            # STEP 4: Wait for results
            try:
                wait.until(EC.visibility_of_element_located((By.ID, 'myTable')))
                take_screenshot(driver, "results_loaded", folder_path)
            except TimeoutException:
                take_screenshot(driver, "results_timeout", folder_path)
                print("❌ Results table didn't load")
                continue

            # STEP 5: Find and process all View links
            try:
                view_elements = wait.until(EC.presence_of_all_elements_located(
                    (By.XPATH, "//a[contains(translate(text(), 'VIEW', 'view'), 'view')]"))
                )

                doc_links = []
                for element in view_elements:
                    href = element.get_attribute('href')
                    if href and ('ViewDocument' in href or '.pdf' in href.lower()) and not any(x in href.lower() for x in ['home', 'search', 'index']):
                        doc_links.append({'element': element, 'href': href, 'text': element.text.strip()})

                if not doc_links:
                    raise NoSuchElementException("No valid document links found")

                for doc in doc_links:
                    try:
                        print(f"➡️ Processing document: {doc['text']} ({doc['href']})")
                        
                        driver.execute_script("window.open(arguments[0]);", doc['href'])
                        driver.switch_to.window(driver.window_handles[1])

                        # ✅ Handle CAPTCHA here
                        handle_captcha_if_present(driver)

                        # Wait briefly for content
                        time.sleep(3)

                        # STEP 6: Save PDF if applicable
                        if any(x in driver.current_url.lower() for x in ['pdf', 'viewer']):
                            try:
                                deed_filename = f"DB_{book}_{int(page)}_{datetime.now().strftime('%H%M%S')}.pdf"
                                deed_path = os.path.join(deeds_folder, deed_filename)

                                # ✅ Attempt to download directly if the URL ends with '.pdf'
                                if driver.current_url.lower().endswith('.pdf'):
                                    response = requests.get(driver.current_url)
                                    if response.status_code == 200:
                                        with open(deed_path, 'wb') as f:
                                            f.write(response.content)
                                        print(f"✅ PDF downloaded directly: {deed_filename}")
                                    else:
                                        raise Exception(f"HTTP {response.status_code} when trying to download PDF")

                                else:
                                    # Fallback to printToPDF if direct download is not straightforward
                                    pdf_data = driver.execute_cdp_cmd("Page.printToPDF", {
                                        "landscape": False,
                                        "printBackground": True
                                    })

                                    with open(deed_path, 'wb') as f:
                                        f.write(base64.b64decode(pdf_data['data']))
                                    print(f"✅ PDF saved using printToPDF: {deed_filename}")

                            except Exception as pdf_error:
                                print(f"❌ PDF save failed, screenshot taken: {pdf_error}")
                                take_screenshot(driver, f"pdf_fallback_{doc['text']}", folder_path)

                        else:
                            print("⚠️ No PDF detected in URL, screenshot taken")
                            take_screenshot(driver, f"non_pdf_{doc['text']}", folder_path)

                    except Exception as e:
                        print(f"❌ Failed to process document: {e}")
                        take_screenshot(driver, "document_process_error", folder_path)
                    finally:
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        time.sleep(1)

            except Exception as e:
                take_screenshot(driver, "view_links_failed", folder_path)
                print(f"❌ Failed to process view links: {e}")
                continue

        except Exception as e_main:
            take_screenshot(driver, "unexpected_error", folder_path)
            print(f"❌ Unexpected error: {e_main}")
            continue
