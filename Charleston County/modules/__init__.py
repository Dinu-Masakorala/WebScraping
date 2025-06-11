# modules/__init__.py
from .property_card import download_property_card
from .deed_info import extract_deed_info
from .tax_info import download_tax_info
from modules.document_download import process_deed_pdfs  # Updated to use process_deed_pdfs

__all__ = [
    'download_property_card',
    'extract_deed_info',
    'download_tax_info',
    'process_deed_pdfs'
]