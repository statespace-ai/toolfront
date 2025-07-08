from pathlib import Path

from toolfront.models.document import Document

MAX_SAMPLE_CHARS = 10000


class RTF(Document):
    """Rich Text Format file."""

    async def sample(self) -> str:
        try:
            from striprtf.striprtf import rtf_to_text

            with Path(self.path).open("r", encoding="utf-8") as file:
                rtf_content = file.read()
                text = rtf_to_text(rtf_content)
                return text[:MAX_SAMPLE_CHARS]
        except ImportError:
            # Fallback to raw RTF if striprtf not available
            with Path(self.path).open("r", encoding="utf-8") as file:
                content = file.read()[:MAX_SAMPLE_CHARS]
                return f"RTF content (requires striprtf library for text extraction):\n{content}"
        except Exception as e:
            return f"Error reading RTF file: {str(e)}"

    async def read(self) -> str:
        try:
            from striprtf.striprtf import rtf_to_text

            with Path(self.path).open("r", encoding="utf-8") as file:
                rtf_content = file.read()
                text = rtf_to_text(rtf_content)
                return text
        except ImportError:
            # Fallback to raw RTF if striprtf not available
            with Path(self.path).open("r", encoding="utf-8") as file:
                return f"RTF content (requires striprtf library for text extraction):\n{file.read()}"
        except Exception as e:
            return f"Error reading RTF file: {str(e)}"
