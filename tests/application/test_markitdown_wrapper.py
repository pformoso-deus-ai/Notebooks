import pytest
import os
from src.application.services.markitdown_wrapper import MarkItDownWrapper

@pytest.fixture
def sample_pdf_file():
    path = os.path.join(os.path.dirname(__file__), '../fixtures/crohn_dda.pdf')
    return os.path.abspath(path)

def test_convert_to_markdown_success(sample_pdf_file):
    wrapper = MarkItDownWrapper()
    result = wrapper.convert_to_markdown(sample_pdf_file)
    assert result is not None
    assert "Crohn's Disease Management" in result
    assert "Patient ID" in result

def test_convert_to_markdown_file_not_found():
    wrapper = MarkItDownWrapper()
    result = wrapper.convert_to_markdown('/nonexistent/file/path.pdf')
    assert result is None 