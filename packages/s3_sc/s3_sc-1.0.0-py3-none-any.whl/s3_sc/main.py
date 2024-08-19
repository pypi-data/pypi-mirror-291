"""Main unit."""
import sys
import configparser

from s3_sc.cli import parse_args, ListObjectArgs, PutObjectArgs, DeleteObjectArgs, GetObjectArgs
from s3_sc.logger import Logging
from s3_sc.config_reader import ConfigReader
from s3_sc.s3_client import S3Client
import asyncio

logger = Logging("s3_client")
s3_config_parser = ConfigReader(logger=logger)

async def init_s3_client(config: str) -> S3Client:
    """Initialize s3 client."""
    try:
        (s3_access_key,
         s3_secret_key,
         s3_endpoint,
         s3_bucket_name) = s3_config_parser.read_s3_config(config)
        s3_client = S3Client(
            access_key=s3_access_key,
            secret_key=s3_secret_key,
            endpoint=s3_endpoint,
            bucket_name=s3_bucket_name,
            logger=logger
        )
        return s3_client
    except (configparser.NoSectionError, configparser.MissingSectionHeaderError):
        logger.error("Can not find section '[main]' in config file: %s", config)
        sys.exit(1)

async def async_main():
    """Async main."""
    cmd_args = parse_args()
    if cmd_args is not None:
        s3_client = await init_s3_client(cmd_args.config)
        if isinstance(cmd_args, ListObjectArgs):
            await s3_client.list_s3_object(cmd_args.s3_file_path)
        elif isinstance(cmd_args, PutObjectArgs):
            await s3_client.put_s3_object(cmd_args.local_file, cmd_args.s3_file_path)
        elif isinstance(cmd_args, GetObjectArgs):
            await s3_client.get_s3_object(cmd_args.s3_file_path, cmd_args.local_file_path)
        elif isinstance(cmd_args, DeleteObjectArgs):
            await s3_client.delete_s3_object(cmd_args.s3_file_path)

def main():
    """Sync main."""
    asyncio.run(async_main())

if __name__ == "__main__":
    main()
