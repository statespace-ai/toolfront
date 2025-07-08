from toolfront.models.document import Document

MAX_SAMPLE_CHARS = 10000


class PowerPoint(Document):
    """Microsoft PowerPoint presentation."""

    async def sample(self) -> str:
        try:
            from pptx import Presentation

            prs = Presentation(self.path)
            text = ""
            for i, slide in enumerate(prs.slides[:5]):  # Sample first 5 slides
                text += f"Slide {i + 1}:\n"
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text += shape.text + "\n"
                text += "\n"
            return text[:MAX_SAMPLE_CHARS]
        except ImportError:
            return "PowerPoint support requires python-pptx library"
        except Exception as e:
            return f"Error reading PowerPoint file: {str(e)}"

    async def read(self) -> str:
        try:
            from pptx import Presentation

            prs = Presentation(self.path)
            text = ""
            for i, slide in enumerate(prs.slides):
                text += f"Slide {i + 1}:\n"
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text += shape.text + "\n"
                text += "\n"
            return text
        except ImportError:
            return "PowerPoint support requires python-pptx library"
        except Exception as e:
            return f"Error reading PowerPoint file: {str(e)}"
