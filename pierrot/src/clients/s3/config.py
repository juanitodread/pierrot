from dataclasses import dataclass


@dataclass
class S3Config:
  bucket: str
