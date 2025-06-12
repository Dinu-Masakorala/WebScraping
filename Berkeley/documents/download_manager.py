import os
import requests

def download_deed_pdf(deed_info, folder_path):
    """Download the deed PDF given the info and save it to folder_path."""
    pdf_url = deed_info.get("pdf_url")
    book = deed_info.get("book")
    page = deed_info.get("page")

    if not pdf_url or not book or not page:
        print("❌ Missing deed information. Skipping download.")
        return

    file_name = f"DB {book} {page}.pdf"
    save_path = os.path.join(folder_path, file_name)

    try:
        response = requests.get(pdf_url)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"✅ Downloaded Deed PDF → {save_path}")
    except Exception as e:
        print(f"❌ Failed to download deed PDF: {e}")
