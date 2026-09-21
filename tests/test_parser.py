from unittest.mock import MagicMock , patch
import httpx
import pytest
from src.parser import RemoteJobParser

class TestRemoteJobParser:
    @patch("httpx.Client.get")
    def test_fetch_from_url_success(self, mock_get):
        # Mock successful HTTP 200 response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Job Description Content: Python, Django, PostgreSQL"
        mock_get.return_value = mock_response


        content = RemoteJobParser.fetch_from_url("https://jobs.example.com/api/101")
        assert "Python" in content
        assert "Django" in content
        mock_get.assert_called_once()


    @patch("httpx.Client.get")
    def test_fetch_from_url_http_error(self, mock_get):
        # Mock 404 HTTP Error
        mock_get.side_effect = httpx.HTTPStatusError(
            "404 Not Found", request=MagicMock(), response=MagicMock()
        )


        with pytest.raises(ConnectionError) as exc_info:
            RemoteJobParser.fetch_from_url("https://jobs.example.com/api/invalid")
        assert "Failed to fetch job posting" in str(exc_info.value)


    @patch("httpx.Client.get")
    def test_fetch_from_url_timeout(self, mock_get):
        # Mock Connection Timeout
        mock_get.side_effect = httpx.ConnectTimeout("Network timed out")


        with pytest.raises(ConnectionError):
            RemoteJobParser.fetch_from_url("https://slow-api.example.com/jobs")


    def test_invalid_url_format(self):
        with pytest.raises(ValueError) as exc_info:
            RemoteJobParser.fetch_from_url("not_a_valid_url")
            assert "Invalid URL" in str(exc_info.value)
