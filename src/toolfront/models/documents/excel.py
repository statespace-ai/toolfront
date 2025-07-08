import pandas as pd

from toolfront.models.document import Document

MAX_SAMPLE_ROWS = 50


class Excel(Document):
    """Microsoft Excel spreadsheet."""

    async def sample(self) -> str:
        try:
            # Read first sheet with limited rows
            df = pd.read_excel(self.path, nrows=MAX_SAMPLE_ROWS)
            return f"Shape: {df.shape}\nColumns: {list(df.columns)}\n\nSample data:\n{df.head().to_string()}"
        except Exception as e:
            return f"Error reading Excel file: {str(e)}"

    async def read(self) -> str:
        try:
            # Read all sheets
            excel_data = pd.read_excel(self.path, sheet_name=None)
            result = ""
            for sheet_name, df in excel_data.items():
                result += f"Sheet: {sheet_name}\n"
                result += f"Shape: {df.shape}\n"
                result += f"Columns: {list(df.columns)}\n"
                result += df.to_string() + "\n\n"
            return result
        except Exception as e:
            return f"Error reading Excel file: {str(e)}"
