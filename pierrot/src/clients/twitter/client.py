import tweepy

from pierrot.src.clients.twitter.config import TwitterConfig
from pierrot.src.errors import PierrotExeception
from pierrot.src.logging import get_logger


log = get_logger(__name__)


class Twitter:
  def __init__(self, config: TwitterConfig) -> None:
    self._config = config

    self._client = tweepy.Client(
      consumer_key=self._config.consumer_key,
      consumer_secret=self._config.consumer_secret,
      access_token=self._config.access_token,
      access_token_secret=self._config.access_token_secret,
    )
    self._api = tweepy.API(tweepy.OAuth1UserHandler(
      consumer_key=self._config.consumer_key,
      consumer_secret=self._config.consumer_secret,
      access_token=self._config.access_token,
      access_token_secret=self._config.access_token_secret,
    ))

  def upload_photo(self, file_name: str) -> str:
    log.info(f'Uploading photo: file_name={file_name}')

    try:
      media = self._api.media_upload(file_name)
      return media.media_id
    except Exception as error:
      raise PierrotExeception(error)

  def publish_tweet(self, photo_id: str, text: str) -> dict:
    log.info(f'Publishing tweet: photo_id={photo_id}, text={text}')

    try:
      response = self._client.create_tweet(text=text, media_ids=[photo_id])
      return response.data
    except Exception as error:
      raise PierrotExeception(error)


class TwitterLocal(Twitter):
  def __init__(self, config: TwitterConfig) -> None:
    self._config = config

  def upload_photo(self, file_name: str) -> str:
    log.info(f'Uploading photo: file_name={file_name}')
    return 'cafebabe'

  def publish_tweet(self, photo_id: str, text: str) -> None:
    log.info(f'Publishing tweet: photo_id={photo_id}, text={text}')
