from unittest.mock import patch, MagicMock

import pytest

from pierrot.src.clients.twitter.client import Twitter
from pierrot.src.clients.twitter.config import TwitterConfig
from pierrot.src.errors import PierrotExeception


@pytest.fixture()
@patch('pierrot.src.clients.twitter.client.tweepy.API')
@patch('pierrot.src.clients.twitter.client.tweepy.Client')
def twitter(tweepy_client_mock, tweepy_api_mock) -> Twitter:
  status = MagicMock()
  status.data = {
    'edit_history_tweet_ids': ['1767726249542332728'],
    'id': '1767726249542332728',
    'text': '📸‼️ \n\n #pierrotPhotography #photography https://t.co/ZXTF7XhiAj'
  }
  tweepy_client_mock.return_value.create_tweet = MagicMock(return_value=status)

  media = MagicMock()
  media.media_id = 'photo-123'
  tweepy_api_mock.return_value.media_upload = MagicMock(return_value=media)

  return Twitter(TwitterConfig(
    consumer_key='consumer-key',
    consumer_secret='consumer-secret',
    access_token='access-token',
    access_token_secret='access-token-secret',
    tweet_text='tweet-text',
  ))


class TestTwitter:
  def test_upload_photo(self, twitter):
    photo_id = twitter.upload_photo(file_name='photo.jpg')

    assert photo_id == 'photo-123'
    twitter._api.media_upload.assert_called_with('photo.jpg')

  def test_upload_photo_when_api_error(self, twitter):
    twitter._api.media_upload.side_effect = Exception('api-error')

    with pytest.raises(PierrotExeception):
      twitter.upload_photo(file_name='photo.jpg')

  def test_publish_tweet(self, twitter):
    response = twitter.publish_tweet(photo_id='photo-id-123', text='first tweet with photo')

    assert response == {
      'edit_history_tweet_ids': ['1767726249542332728'],
      'id': '1767726249542332728',
      'text': '📸‼️ \n\n #pierrotPhotography #photography https://t.co/ZXTF7XhiAj'
    }
    twitter._client.create_tweet.assert_called_with(text='first tweet with photo', media_ids=['photo-id-123'])

  def test_publish_tweet_when_client_error(self, twitter):
    twitter._client.create_tweet.side_effect = Exception('api-error')

    with pytest.raises(PierrotExeception):
      twitter.publish_tweet(photo_id='photo-id-123', text='first tweet with photo')
