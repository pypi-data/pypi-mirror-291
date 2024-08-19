"""CLI module."""
import argparse
from dataclasses import dataclass
from importlib.metadata import version
import os
from typing import Optional, Union


@dataclass
class BasicArgs:
    """Basic class for CLI arguments."""

    config: str

@dataclass
class ListObjectArgs(BasicArgs):
    """Args for listing object in bucket."""

    command: str
    s3_file_path: str

@dataclass
class PutObjectArgs(BasicArgs):
    """Args for put object in bucket."""

    command: str
    local_file: str
    s3_file_path: str

@dataclass
class DeleteObjectArgs(BasicArgs):
    """Args for delete object in bucket."""

    command: str
    s3_file_path: str

@dataclass
class GetObjectArgs(BasicArgs):
    """Args for get object from s3."""

    command: str
    s3_file_path: str
    local_file_path: str

def parse_args() -> Optional[Union[ListObjectArgs, PutObjectArgs, DeleteObjectArgs, GetObjectArgs]]:
    """Create CLI."""
    parser = argparse.ArgumentParser(description="s3_client argument parser")
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {version('s3_sc')}",
        help="s3_client version"
    )
    parser.add_argument(
        "-c", "--config",
        required=True,
        default=os.environ.get("CONFIG_PATH", '~/s3_client.conf'),
        help="Path to s3_client config",
        dest="s3_config"
    )
    subparsers = parser.add_subparsers(
        title="s3_client subcommands",
        description="valid subcommands",
        dest="command"
    )
    ## List Object command
    list_object_parser = subparsers.add_parser(
        "ls", help="Usage <path>. Put </> to start from root."
    )
    list_object_parser.add_argument(
        "s3_file_path",
        help="Path to s3 file or directory"
    )
    ## Put object command
    put_object_parser = subparsers.add_parser(
        "put", help="Usage <path_to_local_file> <path_to_s3_file>"
    )
    put_object_parser.add_argument(
        "local_file",
        help="Path to local file"
    )
    put_object_parser.add_argument(
        "s3_file_path",
        help="Path to file in s3 bucket"
    )
    # Delete object command
    delete_object_parser = subparsers.add_parser(
        "delete", help="Usage <path_to_s3_file>"
    )
    delete_object_parser.add_argument(
        "s3_file_path",
        help="Path to S3 file in bucket"
    )
    # Get object command
    get_object_parser = subparsers.add_parser(
        "get", help="Usage <path_to_s3_file> <path_to_local>"
    )
    get_object_parser.add_argument(
        "s3_file_path",
        help="Path to s3 file"
    )
    get_object_parser.add_argument(
        "local_file_path",
        help="Path to local file to save"
    )

    args = parser.parse_args()

    if args.command == "ls":
        return ListObjectArgs(
            command=args.command,
            config=args.s3_config,
            s3_file_path=args.s3_file_path
        )
    elif args.command == "put":
        return PutObjectArgs(
            command=args.command,
            config=args.s3_config,
            local_file = args.local_file,
            s3_file_path=args.s3_file_path
        )
    elif args.command == "delete":
        return DeleteObjectArgs(
            command=args.command,
            config=args.s3_config,
            s3_file_path=args.s3_file_path
        )
    elif args.command == "get":
        return GetObjectArgs(
            command=args.command,
            config=args.s3_config,
            s3_file_path=args.s3_file_path,
            local_file_path=args.local_file_path
        )
    else:
        parser.print_help()
        return None

