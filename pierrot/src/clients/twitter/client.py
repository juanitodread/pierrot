import tweepy

from pierrot.src.clients.twitter.config import TwitterConfig


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
    print(f'Uploading photo: file_name={file_name}')

    media = self._api.media_upload(file_name)
    return media.media_id

  def publish_tweet(self, photo_id: str, text: str) -> dict:
    print(f'Publishing tweet: photo_id={photo_id}, text={text}')

    response = self._client.create_tweet(text=text, media_ids=[photo_id])
    return response.data


class TwitterLocal(Twitter):
  def __init__(self, config: TwitterConfig) -> None:
    self._config = config

  def upload_photo(self, file_name: str) -> str:
    print(f'Uploading photo: file_name={file_name}')
    return 'cafebabe'

  def publish_tweet(self, photo_id: str, text: str) -> None:
    print(f'Publishing tweet: photo_id={photo_id}, text={text}')
