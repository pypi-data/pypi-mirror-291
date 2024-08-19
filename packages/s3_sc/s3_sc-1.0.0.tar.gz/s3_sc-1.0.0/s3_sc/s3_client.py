"""S3 module."""
from contextlib import asynccontextmanager
from s3_sc.logger import Logging
from aiobotocore.client import AioBaseClient
from aiobotocore.session import get_session, AioSession
from dataclasses import dataclass, field
from botocore.exceptions import ClientError, ConnectTimeoutError, EndpointConnectionError
import sys


@dataclass
class S3Client:
    """S3 client class."""

    access_key: str
    secret_key: str
    endpoint: str
    bucket_name: str
    logger: Logging
    session: AioSession = field(init=False)
    s3_config: dict = field(init=False)

    def __post_init__(self):
        """Add attributes."""
        self.s3_config = {
            "aws_access_key_id": self.access_key,
            "aws_secret_access_key": self.secret_key,
            "endpoint_url": self.endpoint
        }
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self) -> AioBaseClient:
        """Get s3 client."""
        async with self.session.create_client("s3", **self.s3_config) as client:
            yield client

    async def list_s3_object(self, path: str) -> None:
        """List object (file and directory)."""
        try:
            async with self.get_client() as client:
                paginator = client.get_paginator('list_objects_v2')
                pages = paginator.paginate(
                    Bucket=self.bucket_name,
                    Prefix=path.lstrip('/'),
                    Delimiter='/'
                )
                async for page in pages:
                    if "Contents" in page:
                        for obj in page["Contents"]:
                            key = obj["Key"]
                            size = obj["Size"]
                            last_modified = obj["LastModified"]
                            date_str = last_modified.strftime('%Y-%m-%d %H:%M')
                            print(f"FILE {date_str} {size:>10}  s3://{self.bucket_name}/{key}")
                    if "CommonPrefixes" in page:
                        for prefix in page["CommonPrefixes"]:
                            print(f"DIR s3://{self.bucket_name}/{prefix['Prefix']}")
        except (ClientError, ValueError, ConnectTimeoutError, EndpointConnectionError) as err:
            self.logger.error("S3Client error: %s", err)
            sys.exit(1)

    async def put_s3_object(self, src_path: str, dest_path: str) -> None:
        """Put object in bucket."""
        try:
            async with self.get_client() as client:
                with open(src_path, "rb") as file:
                    await client.put_object(
                        Bucket=self.bucket_name,
                        Key=dest_path,
                        Body=file
                    )
                self.logger.info(
                    "Object %s was upload to s3://%s/%s",
                    src_path, self.bucket_name, dest_path
                )
        except (ClientError, ValueError) as err:
            self.logger.error("Error uploading file %s. Error: %s", src_path, err)
            sys.exit(1)

    async def delete_s3_object(self, dest_path: str) -> None:
        """Delete object from bucket."""
        try:

            async with self.get_client() as client:
                if dest_path.endswith("/"):
                    paginator = client.get_paginator("list_objects_v2")
                    pages = paginator.paginate(
                        Bucket=self.bucket_name,
                        Prefix=dest_path
                    )
                    objects_to_delete = []
                    async for page in pages:
                        if "Contents" in page:
                            for obj in page["Contents"]:
                                objects_to_delete.append({'Key': obj['Key']})
                    if objects_to_delete:
                        await client.delete_objects(
                            Bucket=self.bucket_name,
                            Delete={
                                'Objects': objects_to_delete,
                                'Quiet': True
                            }
                        )
                        self.logger.info(
                            "Deleted %d objects from s3://%s/%s",
                            len(objects_to_delete), self.bucket_name, dest_path
                        )
                    else:
                        self.logger.info(
                            "No objects found to delete in s3://%s/%s",
                            self.bucket_name,
                            dest_path
                        )
                else:
                    await client.delete_object(
                        Bucket=self.bucket_name,
                        Key=dest_path
                    )
                    self.logger.info(
                        "Deleted single object s3://%s/%s",
                        self.bucket_name, dest_path
                    )
        except (ClientError, ValueError) as err:
            self.logger.error("Error deleting object %s. Error: %s", dest_path, err)
            sys.exit(1)

    async def get_s3_object(self, dest_path: str, src_path: str) -> None:
        """Get object from bucket."""
        try:
            async with self.get_client() as client:
                response = await client.get_object(
                    Bucket=self.bucket_name,
                    Key=dest_path
                )
                obj_data = await response["Body"].read()
                with open(src_path, "wb") as file:
                    file.write(obj_data)
                self.logger.info("Object %s was save to %s", dest_path, src_path)
        except (ClientError, ValueError) as err:
            self.logger.error("Error saving object %s. Error: %s", dest_path, err)
            sys.exit(1)
