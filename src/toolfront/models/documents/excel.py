import logging

from toolfront.models.documents.base import Document, DocumentError

logger = logging.getLogger("toolfront")


class ExcelDocument(Document):
    """Excel document reader."""

    async def read(self, pagination: int | float = 0) -> str:
        """Read Excel document content.

        Args:
            pagination: Sheet number (1+ int) or percentile (0-1 exclusive float) to read.

        Returns:
            Document content as string.
        """
        try:
            import pandas as pd

            excel_data = pd.read_excel(self.path, sheet_name=None)
            sheet_names = list(excel_data.keys())
            total_sheets = len(sheet_names)

            target_sheet_idx = self._get_target_page(pagination, total_sheets) - 1
            target_sheet_name = sheet_names[target_sheet_idx]
            df = excel_data[target_sheet_name]

            result = f"Sheet {target_sheet_idx + 1} of {total_sheets}: {target_sheet_name}\n"
            result += f"Shape: {df.shape}\n"
            result += f"Columns: {list(df.columns)}\n"
            result += df.to_string() + "\n"

            return result
        except ImportError:
            error_msg = "Excel support requires pandas and openpyxl libraries"
            logger.error(f"Missing dependency for Excel reading: {error_msg}")
            raise DocumentError(error_msg)
        except Exception as e:
            logger.error(f"Error reading Excel file {self.url}: {e}")
            raise DocumentError(f"Error reading Excel file: {str(e)}")
