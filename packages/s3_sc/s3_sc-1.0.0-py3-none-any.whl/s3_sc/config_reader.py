"""Config reader module."""
import configparser
import os.path
from dataclasses import dataclass
from s3_sc.logger import Logging
import sys


@dataclass
class ConfigReader:
    """Read config file."""

    logger: Logging
    config_parser: configparser.ConfigParser = configparser.ConfigParser()

    def read_s3_config(self, s3_config: str) -> tuple[str, str, str, str]:
        """Read s3 config."""
        if os.path.isfile(s3_config):
            self.config_parser.read(s3_config)
            s3_access_key = self.config_parser.get("main", "S3_ACCESS_KEY")
            s3_secret_key = self.config_parser.get("main", "S3_SECRET_KEY")
            s3_endpoint = self.config_parser.get("main", "S3_ENDPOINT")
            s3_bucket_name = self.config_parser.get("main", "S3_BUCKET_NAME")
            return s3_access_key, s3_secret_key, s3_endpoint, s3_bucket_name
        else:
            self.logger.error("Config file: %s does not exist", s3_config)
            sys.exit(1)
