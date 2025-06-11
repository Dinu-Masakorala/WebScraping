Property Deed & Tax Info Scraper

This project automates the extraction of property deed book/page numbers and tax information from a public website using Selenium. It handles CAPTCHAs, stale elements, PDF downloads, and errors via screenshots for debugging.

📂 Features
Extract deed book and page numbers
Download deed documents (PDFs)
Download property tax information (PDF)
Handles CAPTCHAs (manual solving)
Stale element error handling
Automatic screenshot capture for errors

⚙️ Setup Instructions
1️⃣ Clone the Repository

2️⃣ Install Requirements
Ensure Python 3.8+ is installed.
3️⃣ Configure config.py
Update the DEED_SEARCH_URL and BASE_OUTPUT_DIR in config.py to the deed search website of your target county/region and the folder path you want download pdfs.
Example:
DEED_SEARCH_URL = "https://example.gov/DeedSearch"

4️⃣ Setup WebDriver
Download the appropriate ChromeDriver for your Chrome version: https://chromedriver.chromium.org/downloads
Make sure it’s in your PATH or specify its location in your script.

▶️ Running the Project
python main.py

Error screenshots: Saved in the /errors folder inside your output directory.
Deeds PDFs: Saved in the /deeds folder inside your output directory.
Tax Info PDF: Named Tax Info.pdf in the same directory.

❗ CAPTCHA Handling
If a CAPTCHA is detected:
Solve it manually in the browser window.
Press Enter in your terminal when prompted to resume the script.

📝 Customization
Target URL: Update in config.py
Output Folder: Modify in your main execution script as needed.
Timeouts & Wait Times: Adjustable in code for sites with different response speeds.
