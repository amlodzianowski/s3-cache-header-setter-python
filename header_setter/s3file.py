"""S3 File Class."""
from typing import TYPE_CHECKING

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

from header_setter.settings import CACHE_CONTROL_VALUE

if TYPE_CHECKING:
    from mypy_boto3_s3 import S3ServiceResource, S3Client
    from mypy_boto3_s3.type_defs import CopyObjectOutputTypeDef, ResponseMetadataTypeDef
else:
    S3Client = object
    S3ServiceResource = object
    CopyObjectOutputTypeDef = object
    ResponseMetadataTypeDef = object


class InaccessibleFile(Exception):
    """Inaccessible S3 File Exception."""


s3_resource = boto3.resource("s3")
s3_client = boto3.client("s3")


class S3File:
    """S3 File Class."""

    def __init__(
        self, bucket_name: str, key: str, s3_res: S3ServiceResource = s3_resource
    ) -> None:
        """Class Init."""
        self.s3_resource = s3_res
        self.file = self.s3_resource.Object(bucket_name, key)

    @property
    def cache_control_configured(self) -> bool:
        """Is cache control configured on an object.

        Raises:
            InaccessibleFile: Inaccessible S3 File Exception

        Returns:
            bool: Cache control configured?
        """
        try:
            return self.file.cache_control is not None
        except (ClientError, NoCredentialsError) as err:
            raise InaccessibleFile(f"Unable to access object metadata: {err}") from err

    def configure_cache_control(
        self, s3_boto3_client: S3Client = s3_client
    ) -> ResponseMetadataTypeDef:
        """Overwrite object in S3 with new metadata containing the cache control setting.

        Args:
            s3_boto3_client (S3Client, optional): Boto3 S3 Client. Defaults to s3_client.

        Returns:
            ResponseMetadataTypeDef: Copy Object Response Metadata
        """
        res: CopyObjectOutputTypeDef = s3_boto3_client.copy_object(
            Bucket=self.file.bucket_name,
            CopySource={"Bucket": self.file.bucket_name, "Key": self.file.key},
            Key=self.file.key,
            CacheControl=CACHE_CONTROL_VALUE,
            ContentType=self.file.content_type,
            MetadataDirective="REPLACE",
            Metadata=self.file.metadata,
            TaggingDirective="COPY",
        )
        return res["ResponseMetadata"]
