"""Handler unit tests."""
from unittest import TestCase
from typing import Any

import json
from header_setter.handler import handler


class TestHandler(TestCase):
    """Unit tests for handler."""

    s3_event: dict[str, Any] = {}

    @classmethod
    def setUpClass(cls) -> None:
        """Test class setup."""
        with open("tests/fixtures/s3_event.json", "r", encoding="utf-8") as f_handle:
            cls.s3_event = json.load(f_handle)

    def test_handler(self) -> None:
        """Test handler."""
        res = handler(self.s3_event, {})
        expected = "Hello World! my-s3-bucket"
        self.assertEqual(res, expected)
