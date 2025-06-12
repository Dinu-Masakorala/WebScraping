import pandas as pd
import os
import logging


def load_tms_numbers(filepath="data/Master Excel sheet (for task_one).xlsx"):
    """
    Loads TMS numbers from the specified Excel file.
    Returns a list of non-empty, string-converted TMS numbers.
    """
    df = pd.read_excel(filepath)
    df['Berkeley'] = df['Berkeley'].apply(lambda x: str(int(x)) if pd.notna(x) else '')
    return df['Berkeley'][df['Berkeley'] != ''].tolist()


def create_folder(path):
    """
    Creates a folder at the specified path if it doesn't already exist.
    """
    os.makedirs(path, exist_ok=True)
    return path


def create_tms_folder(tms_number):
    """
    Creates and returns the path to a folder for the given TMS number.
    """
    folder = os.path.join(os.getcwd(), "downloads", str(tms_number))
    return create_folder(folder)


def save_results(results, filename="results/berkeley_full_results.xlsx"):
    """
    Saves the results list of dictionaries to an Excel file.
    """
    df = pd.DataFrame(results)
    create_folder(os.path.dirname(filename))
    df.to_excel(filename, index=False)
    print(f"✅ Results saved to → {filename}")


def setup_logging(log_file="berkeley.log"):
    """
    Sets up logging configuration.
    Logs will be written to both a file and the console.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s — %(levelname)s — %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
