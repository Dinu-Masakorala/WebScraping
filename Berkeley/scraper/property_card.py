from selenium.webdriver.common.by import By
import base64, os, re
from utils.helpers import create_tms_folder


def download_property_card(driver, property_data):
    """
    Downloads the Property Card PDF for a given property and extracts Book/Page info.
    """
    tms_number = property_data.get("tms_number")
    if not tms_number:
        raise ValueError("TMS number is missing in property_data")

    folder_path = create_tms_folder(tms_number)

    url = f"https://berkeleycountysc.gov/propcards/property_card.php?tms={tms_number}"
    driver.get(url)

    print(f"Opening Property Card page for TMS: {tms_number}")
    print("⚠️ Solve CAPTCHA manually in the browser window if it appears...")
    input("✅ Press ENTER here AFTER you solve the CAPTCHA and the page loads...")

    # Save Property Card as PDF
    pdf_data = driver.execute_cdp_cmd("Page.printToPDF", {"landscape": False, "printBackground": True})
    pdf_path = os.path.join(folder_path, "Property Card.pdf")
    with open(pdf_path, "wb") as f:
        f.write(base64.b64decode(pdf_data["data"]))

    print(f"✅ Saved Property Card → {pdf_path}")

    # Extract Book/Page info
    # Find all elements containing "Deed Book" in their text anywhere on the page
    print("🔍 Searching for all elements containing text 'Deed Book'...")
    elements_with_text = driver.find_elements(By.XPATH, "//*[contains(text(), 'Deed Book')]")
    if elements_with_text:
        print(f"✅ Found {len(elements_with_text)} element(s) containing 'Deed Book':")
        for i, el in enumerate(elements_with_text, start=1):
            try:
                text = el.text.strip()
            except Exception:
                text = "(unable to retrieve text)"
            print(f"  [{i}] Text: {text}")
    else:
        print("❌ No elements found containing 'Deed Book' text.")
    # Given XPaths list
    xpaths = [
        "/html/body/table[4]/tbody/tr[1]/td[4]/b",
        "/html/body/table[4]/html/body/table[4]/tbody/tr[1]/td[4]/b",
        "/html/body/table[4]/html/body/table[4]/html/body/table[4]/tbody/tr[1]/td[4]/b"
    ]
    print("\n🔍 Searching elements by given XPaths...")
    found_any = False

    if not book_page_text:
        return {"TMS": tms_number, "Book_Page": "Not Found"}

    match = re.match(r"(\d+)\s*/\s*(\d+)", book_page_text)
    if match:
        return {
            "TMS": tms_number,
            "Book_Page": book_page_text,
            "Book": match.group(1),
            "Page": match.group(2).zfill(3),
            "PDF_Path": pdf_path
        }
    else:
        return {"TMS": tms_number, "Book_Page": book_page_text, "Deed_PDF": "Invalid Book/Page"}
