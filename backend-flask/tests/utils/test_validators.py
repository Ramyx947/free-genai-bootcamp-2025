from unittest.mock import MagicMock

import pytest
from flask import Request

from app.utils.validators import validate_request_data


def test_validate_request_data():
    """Test validation of request data"""
    # Create a mock Flask request
    mock_request = MagicMock(spec=Request)
    mock_request.is_json = True
    mock_request.get_json.return_value = {"prompt": "Test prompt"}

    # Test valid request
    result = validate_request_data(mock_request)
    assert result == {"prompt": "Test prompt"}

    # Test invalid request - not JSON
    mock_request.is_json = False
    with pytest.raises(ValueError):
        validate_request_data(mock_request)

    # Test invalid request - missing prompt
    mock_request.is_json = True
    mock_request.get_json.return_value = {}
    # The validator returns None for empty data
    result = validate_request_data(mock_request)
    assert result is None
