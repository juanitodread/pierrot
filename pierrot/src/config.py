import os


class Config:
  FLICKR_API_KEY = os.getenv('FLICKR_API_KEY')
  FLICKR_API_SECRET = os.getenv('FLICKR_API_SECRET')

  AWS_S3_PIERROT_KEY = os.getenv('AWS_PIERROT_KEY')
  AWS_S3_PIERROT_SECRET = os.getenv('AWS_PIERROT_SECRET')
  AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET')

  TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
  TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
  TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
  TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

  @staticmethod
  def get_flickr_config() -> None:
    return None

  @staticmethod
  def get_s3_config() -> None:
    return None

  @staticmethod
  def get_twitter_config() -> None:
    return None
