import csv
from pathlib import Path

import pandas as pd
from pypdfium2 import PdfDocument

from toolfront.models.document import Document

MAX_SAMPLE_PAGES = 3
PAGE_SAMPLE_SIZE = 1000
MAX_SAMPLE_CHARS = 10000
MAX_SAMPLE_ROWS = 50


class PDF(Document):
    """PDF document."""

    async def sample(self) -> str:
        doc = PdfDocument(self.path)
        text = ""
        for page in doc:
            text += "Page " + str(page.number) + ": " + page.get_text()[:PAGE_SAMPLE_SIZE] + "...\n"
        doc.close()
        return text

    async def read(self) -> str:
        doc = PdfDocument(self.path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text


class CSV(Document):
    """CSV file."""

    async def sample(self) -> str:
        try:
            df = pd.read_csv(self.path, nrows=MAX_SAMPLE_ROWS)
            return f"Shape: {df.shape}\nColumns: {list(df.columns)}\n\nSample data:\n{df.head().to_string()}"
        except Exception:
            # Fallback to basic CSV reading
            with Path(self.path).open("r", encoding="utf-8") as file:
                reader = csv.reader(file)
                lines = []
                for i, row in enumerate(reader):
                    if i >= MAX_SAMPLE_ROWS:
                        break
                    lines.append(",".join(row))
                return "\n".join(lines)

    async def read(self) -> str:
        try:
            df = pd.read_csv(self.path)
            return f"Shape: {df.shape}\nColumns: {list(df.columns)}\n\nData:\n{df.to_string()}"
        except Exception:
            # Fallback to basic CSV reading
            with Path(self.path).open("r", encoding="utf-8") as file:
                return file.read()
