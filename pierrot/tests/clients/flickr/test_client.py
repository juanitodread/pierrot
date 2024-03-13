from unittest.mock import patch, MagicMock

import pytest

from pierrot.src.clients.flickr.client import Flickr
from pierrot.src.clients.flickr.config import FlickrConfig


@pytest.fixture
def get_config() -> FlickrConfig:
  return FlickrConfig('api_key', 'api_secret')


class TestFlickr:

  @patch('pierrot.src.clients.flickr.client.requests')
  def test_get_photos_total(self, requests_mock, get_config):
    requests_mock.get.return_value = self._build_response_mock(
      json={'photos': {'total': 43}},
    )

    flickr = Flickr(get_config)
    photos = flickr.get_photos_total('akira')

    assert photos == {'photos': 43}

  @patch('pierrot.src.clients.flickr.client.requests')
  def test_get_photos_total_when_server_error(self, requests_mock, get_config):
    requests_mock.get.return_value = self._build_response_mock(
      code=500,
    )

    flickr = Flickr(get_config)
    photos = flickr.get_photos_total('akira')

    assert photos is None

  @patch('pierrot.src.clients.flickr.client.requests')
  def test_get_photos_total_when_invalid_config(self, requests_mock):
    requests_mock.get.return_value = self._build_response_mock(
      code=200,
      text='invalid API key',
      json={'code': 401},
    )

    flickr = Flickr(FlickrConfig('invalid-api-key', 'invalid-secret'))
    photos = flickr.get_photos_total('akira')

    assert photos is None

  @patch('pierrot.src.clients.flickr.client.requests')
  def test_get_photos_metadata(self, requests_mock, get_config):
    requests_mock.get.side_effect = [
      self._build_response_mock(
        code=200,
        json={
          'photos': {
            'photo': [
              {
                'id': '1',
                'title': 'foto-1',
                'o_width': 1,
                'o_height': 1,
                'originalformat': 'jpg',
                'tags': 'tag11 tag12',
                'url_k': 'http://flickr.static.com/1',
                'width_k': 1,
                'height_k': 1,
                'owner': 'akira',
                'pathalias': 'pathalias',
              },
            ],
            'pages': 2,
          },
        },
      ),
      self._build_response_mock(
        code=200,
        json={
          'photos': {
            'photo': [
              {
                'id': '2',
                'title': 'foto-2',
                'ispublic': 1,
                'o_width': 2,
                'o_height': 2,
                'originalformat': 'jpg',
                'tags': 'tag21 tag22',
                'url_k': 'http://flickr.static.com/2',
                'width_k': 2,
                'height_k': 2,
                'owner': 'akira',
                'pathalias': 'pathalias',
              },
            ],
            'pages': 2,
          },
        },
      ),
    ]

    flickr = Flickr(get_config)
    photos = flickr.get_photos_metadata('akira')

    assert photos is not None

    photo1 = photos['1']
    assert photo1['id'] == '1'
    assert photo1['title'] == 'foto-1'
    assert photo1['is_public'] is False
    assert photo1['original_width'] == 1
    assert photo1['original_height'] == 1
    assert photo1['original_format'] == 'jpg'
    assert photo1['tags'] == ['tag11', 'tag12']
    assert photo1['url'] == 'http://flickr.static.com/1'
    assert photo1['width'] == 1
    assert photo1['height'] == 1
    assert photo1['owner'] == 'akira'
    assert photo1['owner_alias'] == 'pathalias'
    assert 'pierrot_timestamp' in photo1

    photo2 = photos['2']
    assert photo2['id'] == '2'
    assert photo2['title'] == 'foto-2'
    assert photo2['is_public'] is True
    assert photo2['original_width'] == 2
    assert photo2['original_height'] == 2
    assert photo2['original_format'] == 'jpg'
    assert photo2['tags'] == ['tag21', 'tag22']
    assert photo2['url'] == 'http://flickr.static.com/2'
    assert photo2['width'] == 2
    assert photo2['height'] == 2
    assert photo2['owner'] == 'akira'
    assert photo2['owner_alias'] == 'pathalias'
    assert 'pierrot_timestamp' in photo2

  @patch('pierrot.src.clients.flickr.client.requests')
  def test_get_photos_metadata_when_server_error(self, requests_mock, get_config):
    requests_mock.get.return_value = self._build_response_mock(
      code=500,
    )

    flickr = Flickr(get_config)
    photos = flickr.get_photos_metadata('akira')

    assert photos is None

  @patch('pierrot.src.clients.flickr.client.requests')
  def test_get_photos_metadata_when_invalid_config(self, requests_mock):
    requests_mock.get.return_value = self._build_response_mock(
      code=200,
      text='invalid API key',
      json={'code': 401},
    )

    flickr = Flickr(FlickrConfig('invalid-api-key', 'invalid-secret'))
    photos = flickr.get_photos_metadata('akira')

    assert photos is None

  def _build_response_mock(self,
                           code: int = 200,
                           text: str = '',
                           json: dict = None):
    response_mock = MagicMock()
    response_mock.status_code = code
    response_mock.text = text
    response_mock.json.return_value = json if json else {}

    return response_mock
