import os

from pierrot.src.clients.flickr.config import FlickrConfig
from pierrot.src.clients.s3.config import S3Config
from pierrot.src.clients.twitter.config import TwitterConfig


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
    )
