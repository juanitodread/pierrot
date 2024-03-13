import os

from pierrot.src.clients.flickr.config import FlickrConfig
from pierrot.src.clients.s3.config import S3Config


class Config:
  FLICKR_API_KEY = os.getenv('FLICKR_API_KEY')
  FLICKR_API_SECRET = os.getenv('FLICKR_API_SECRET')

  AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET')

  TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
  TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
  TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
  TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

  @staticmethod
  def get_flickr_config() -> FlickrConfig:
    return FlickrConfig(
      api_key=Config.FLICKR_API_KEY,
      api_secret=Config.FLICKR_API_SECRET,
    )

  @staticmethod
  def get_s3_config() -> S3Config:
    return S3Config(
      bucket=Config.AWS_S3_BUCKET,
    )

  @staticmethod
  def get_twitter_config() -> None:
    return None
