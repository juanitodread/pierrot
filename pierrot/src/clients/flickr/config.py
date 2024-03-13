from dataclasses import dataclass


@dataclass
class FlickrConfig:
  api_key: str
  api_secret: str
  photos_owner: str
