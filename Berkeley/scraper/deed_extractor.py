from selenium.webdriver.common.by import By
import base64, os


def extract_deed_info(driver, prop_result):
    """
    Downloads the deed PDF for a given property using its Book and Page numbers.
    """
    tms_number = prop_result.get("TMS")
    book = prop_result.get("Book")
    page = prop_result.get("Page")

    if not (tms_number and book and page):
        raise ValueError("Property result must contain 'TMS', 'Book', and 'Page'.")

    folder_path = os.path.join(os.getcwd(), "downloads", str(tms_number))
    os.makedirs(folder_path, exist_ok=True)

    url = "https://search.berkeleydeeds.com/NameSearch.php?Accept=Accept"
    driver.get(url)

    # Fill in Book and Page numbers to search
    driver.wait.until(lambda d: d.find_element(By.XPATH, '//*[@id="bnum"]')).send_keys(book)
    driver.find_element(By.XPATH, '//*[@id="bpagenum"]').send_keys(page)
    driver.find_element(By.XPATH, '//*[@id="searchBtn"]').click()

    try:
        # Wait for the PDF link to appear and retrieve its URL
        pdf_link = driver.wait.until(lambda d: d.find_element(By.PARTIAL_LINK_TEXT, ".pdf"))
        pdf_link_url = pdf_link.get_attribute("href")
        print(f"📥 Found Deed PDF link: {pdf_link_url}")

        # Download and save the PDF using Chrome DevTools Protocol
        deed_pdf = driver.execute_cdp_cmd("Page.printToPDF", {"landscape": False, "printBackground": True})
        deed_path = os.path.join(folder_path, f"DB {book} {page}.pdf")

        with open(deed_path, "wb") as f:
            f.write(base64.b64decode(deed_pdf["data"]))

        print(f"✅ Saved Deed PDF → {deed_path}")

        return {"Deed_PDF": "Saved", "Deed_Path": deed_path}
    except:
        print(f"❗ No PDF link found for Book {book} Page {page}")
        return {"Deed_PDF": "Not Found"}
