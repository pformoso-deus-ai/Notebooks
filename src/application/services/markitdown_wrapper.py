from markitdown import MarkItDown
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class MarkItDownWrapper:
    """
    Wrapper for MarkItDown document conversion.

    Example:
        md = MarkItDownWrapper()
        markdown_text = md.convert_to_markdown('path/to/file.pdf')
    """
    def __init__(self, enable_plugins: bool = False, docintel_endpoint: Optional[str] = None):
        self.md = MarkItDown(enable_plugins=enable_plugins, docintel_endpoint=docintel_endpoint)

    def convert_to_markdown(self, file_path: str) -> Optional[str]:
        """
        Convert a supported file (PDF, DOCX, etc.) to Markdown text.
        Returns the Markdown string, or None if conversion fails.
        """
        try:
            result = self.md.convert(file_path)
            return result.text_content
        except Exception as e:
            logger.error(f"MarkItDown conversion failed for {file_path}: {e}")
            return None 