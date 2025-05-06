import pandas as pd
import os
from config import OUTPUT_DIR

class FileHandler:
    """Handles file operations like reading and writing CSV."""
    
    @staticmethod
    def get_file_path(file_name):
        """Get full file path."""
        return os.path.join(OUTPUT_DIR, file_name)

    @staticmethod
    def read_csv(file_name):
        """Read CSV file after checking validity."""
        path = FileHandler.get_file_path(file_name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"❌ File not found: {path}")
        if os.path.getsize(path) == 0:
            raise ValueError(f"❌ File is empty: {path}")
        return pd.read_csv(path, low_memory=False)

    @staticmethod
    def read_excel(file_name, sheet_name=None):
        """Read Excel file."""
        path = FileHandler.get_file_path(file_name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"❌ File not found: {path}")
        return pd.read_excel(path, sheet_name=sheet_name)
