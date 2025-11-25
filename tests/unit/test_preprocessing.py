"""Tests for preprocessing module."""
import pytest

from app.core.preprocessing import clean_text, preprocess_text


def test_clean_text():
    """Test text cleaning."""
    assert clean_text("  hello   world  ") == "hello world"
    assert clean_text("test\n\n\ntest") == "test test"
    assert clean_text("") == ""


def test_preprocess_text():
    """Test text preprocessing."""
    result = preprocess_text("  Hello   World  ")
    assert result == "hello world"
    assert preprocess_text("") == ""
    assert preprocess_text("TEST") == "test"


def test_preprocess_text_with_special_chars():
    """Test preprocessing with special characters."""
    text = "This is a test!!!"
    result = preprocess_text(text)
    assert isinstance(result, str)
    assert len(result) > 0

