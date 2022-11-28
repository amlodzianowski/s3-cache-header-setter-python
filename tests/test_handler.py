"""Handler unit tests."""
from unittest import TestCase, mock
from typing import Any

import json
from header_setter.handler import handler
from header_setter.s3file import InaccessibleFile


class TestHandler(TestCase):
    """Unit tests for handler."""

    s3_event: dict[str, Any] = {}

    @classmethod
    def setUpClass(cls) -> None:
        """Test class setup."""
        with open("tests/fixtures/s3_event.json", "r", encoding="utf-8") as f_handle:
            cls.s3_event = json.load(f_handle)

    @mock.patch("header_setter.handler.S3File", autospec=True)
    def test_handler_cache_set(self, s3file_mock: mock.Mock) -> None:
        """Test handler cache already set."""
        s3file_mock.return_value.cache_control_configured = True
        res = handler(self.s3_event, {})
        expected = "File: my-s3-bucket/testpath/subfolder/HappyFace.jpg already has a cache control setting"
        self.assertEqual(res, expected)

    @mock.patch("header_setter.handler.S3File")
    def test_handler_cache_not_set(self, s3file_mock: mock.Mock) -> None:
        """Test handler cache not set."""
        s3file_mock.return_value.cache_control_configured = False
        res = handler(self.s3_event, {})
        expected = "Configured cache control on file: my-s3-bucket/testpath/subfolder/HappyFace.jpg"
        self.assertEqual(res, expected)
        s3file_mock.return_value.configure_cache_control.assert_called_once()

    @mock.patch("header_setter.handler.S3File", autospec=True)
    def test_handler_bad_file(self, s3file_mock: mock.Mock) -> None:
        """Test handler bad file."""
        type(s3file_mock.return_value).cache_control_configured = mock.PropertyMock(
            side_effect=InaccessibleFile(
                "Unable to access object metadata: An error occurred"
            )
        )
        res = handler(self.s3_event, {})
        expected = (
            "Unable to process file: my-s3-bucket/testpath/subfolder/HappyFace.jpg. "
            "Error: Unable to access object metadata: An error occurred"
        )
        self.assertEqual(res, expected)
