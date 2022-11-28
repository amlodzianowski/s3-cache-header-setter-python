"""Handler unit tests."""
from unittest import TestCase
import boto3
from moto import mock_s3

from header_setter.s3file import S3File, InaccessibleFile
from header_setter.settings import CACHE_CONTROL_VALUE


class TestS3File(TestCase):
    """Unit tests for handler."""

    bucket_name: str = "my-s3-bucket"
    s3_key: str = "testpath/subfolder/HappyFace.jpg"
    s3_key_no_cache: str = "testpath/subfolder/SadFace.jpg"
    s3_resource = boto3.resource("s3")
    s3_client = boto3.client("s3")
    mock_s3 = mock_s3()

    @classmethod
    def setUpClass(cls) -> None:
        """Test class setup."""
        cls.maxDiff = 500
        cls.mock_s3.start()
        cls.s3_resource = boto3.resource("s3")
        cls.s3_resource.create_bucket(Bucket=cls.bucket_name)
        bucket = cls.s3_resource.Bucket(cls.bucket_name)
        bucket.put_object(Key=cls.s3_key, CacheControl=CACHE_CONTROL_VALUE)
        bucket.put_object(Key=cls.s3_key_no_cache)
        cls.s3_client = boto3.client("s3")

    @classmethod
    def tearDownClass(cls) -> None:
        """Test class teardown."""
        cls.mock_s3.stop()

    def test_cache_control_configured_existing_set(self) -> None:
        """Test cache_control_configured if file already has it configured."""
        file = S3File(self.bucket_name, self.s3_key, self.s3_resource)
        res = file.cache_control_configured
        self.assertTrue(res)

    def test_cache_control_configured_existing_not_set(self) -> None:
        """Test cache_control_configured if file exists but it is not configured."""
        file = S3File(self.bucket_name, self.s3_key_no_cache, self.s3_resource)
        res = file.cache_control_configured
        self.assertFalse(res)

    def test_cache_control_configured_bad_file(self) -> None:
        """Test cache_control_configured if file cannot be accessed."""
        file = S3File(self.bucket_name, "test_file_path", self.s3_resource)
        with self.assertRaisesRegex(
            InaccessibleFile,
            r"^Unable to access object metadata: An error occurred \(404\).*",
        ):
            file.cache_control_configured  # pylint: disable=pointless-statement

    def test_configure_cache_control(self) -> None:
        """Test configure_cache_control."""
        file = S3File(self.bucket_name, self.s3_key_no_cache, self.s3_resource)
        self.assertFalse(file.cache_control_configured)
        res = file.configure_cache_control(self.s3_client)
        self.assertEqual(res["HTTPStatusCode"], 200)
        file_refreshed = S3File(
            self.bucket_name, self.s3_key_no_cache, self.s3_resource
        )
        self.assertTrue(file_refreshed.cache_control_configured)
