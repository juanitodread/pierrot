import os

from pierrot.src.clients.flickr.config import FlickrConfig
from pierrot.src.clients.s3.config import S3Config
from pierrot.src.clients.twitter.config import TwitterConfig
from pierrot.src.clients.bluesky.config import BlueskyConfig


class Config:
  FLICKR_API_KEY = os.getenv('FLICKR_API_KEY')
  FLICKR_API_SECRET = os.getenv('FLICKR_API_SECRET')
  FLICKR_PHOTOS_OWNER = os.getenv('FLICKR_PHOTOS_OWNER')

  AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET')

  TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
  TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
  TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
  TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
  TWITTER_TWEET_TEXT = os.getenv('TWITTER_TWEET_TEXT', '')
  TWITTER_CONFIG_USE_MOCK = os.getenv('TWITTER_CONFIG_USE_MOCK', 'True') == 'True'

  BLUESKY_USERNAME = os.getenv('BLUESKY_USERNAME')
  BLUESKY_APP_PASSWORD = os.getenv('BLUESKY_APP_PASSWORD')
  BLUESKY_CONFIG_USE_MOCK = os.getenv('BLUESKY_CONFIG_USE_MOCK', 'True') == 'True'

  @staticmethod
  def get_flickr_config() -> FlickrConfig:
    return FlickrConfig(
      api_key=Config.FLICKR_API_KEY,
      api_secret=Config.FLICKR_API_SECRET,
      photos_owner=Config.FLICKR_PHOTOS_OWNER,
    )

  @staticmethod
  def get_s3_config() -> S3Config:
    return S3Config(
      bucket=Config.AWS_S3_BUCKET,
    )

  @staticmethod
  def get_twitter_config() -> TwitterConfig:
    return TwitterConfig(
      consumer_key=Config.TWITTER_CONSUMER_KEY,
      consumer_secret=Config.TWITTER_CONSUMER_SECRET,
      access_token=Config.TWITTER_ACCESS_TOKEN,
      access_token_secret=Config.TWITTER_ACCESS_TOKEN_SECRET,
      tweet_text=Config.TWITTER_TWEET_TEXT,
      use_mock=Config.TWITTER_CONFIG_USE_MOCK,
    )

  @staticmethod
  def get_bluesky_config() -> BlueskyConfig:
    return BlueskyConfig(
      username=Config.BLUESKY_USERNAME,
      password=Config.BLUESKY_APP_PASSWORD,
      use_mock=Config.BLUESKY_CONFIG_USE_MOCK,
    )
