from unittest.mock import patch, mock_open, MagicMock

import pytest

from pierrot.src.clients.bluesky.client import Bluesky
from pierrot.src.clients.bluesky.config import BlueskyConfig
from pierrot.src.errors import PierrotException


@pytest.fixture()
@patch('pierrot.src.clients.bluesky.client.Client')
def bluesky(bluesky_client_mock) -> Bluesky:
  bluesky_client_mock.return_value.send_image = MagicMock()

  return Bluesky(BlueskyConfig(username='username', password='password'))


class TestBluesky:

  @patch('builtins.open', new_callable=mock_open, read_data='file_content')
  def test_publish_post(self, mock_file, bluesky):
    bluesky.publish_post('tmp/photo.jpg', 'New photo')

    mock_file.assert_called_once_with('tmp/photo.jpg', 'rb')
    bluesky._client.send_image.assert_called_once()

  def test_publish_post_when_photo_open_error(self, bluesky):
    with pytest.raises(PierrotException):
      bluesky.publish_post('tmp/photo.jpg', 'New photo')

  @patch('builtins.open', new_callable=mock_open, read_data='file_content')
  def test_publish_post_when_client_error(self, mock_file, bluesky):
    bluesky._client.send_image.side_effect = Exception('client-error')

    with pytest.raises(PierrotException):
      bluesky.publish_post('tmp/photo.jpg', 'New photo')
