from typing import Any
from datetime import datetime
import shutil

import requests
import urllib.request

from pierrot.src.clients.flickr.config import FlickrConfig
from pierrot.src.logging import get_logger


type PhotoTotal = dict[str, int]
type PhotoMeta = dict[str, Any]


log = get_logger(__name__)


class Flickr:
  API_URL = 'https://api.flickr.com/services/rest'

  def __init__(self, config: FlickrConfig) -> None:
    self._config = config

  def get_photos_total(self, user: str) -> PhotoTotal | None:
    log.info(f'Getting photos total of user: user={user}')

    params = self._get_photos_params(user, per_page=1)

    log.debug('URL: %s', Flickr.API_URL)
    log.debug('PARAMS: %s', params)
    response = requests.get(url=Flickr.API_URL, params=params)

    if response.status_code != 200:
      log.error('failed calling API: %s', response.text)
      return None

    total_photos = response.json()

    if 'code' in total_photos and total_photos['code'] != 200:
      log.error('API returned error: %s', response.text)
      return None

    return {
      'photos': total_photos['photos']['total']
    }

  def get_photos_metadata(self, user: str) -> dict[str, PhotoMeta] | None:
    log.info(f'Getting photos metadata of user: user={user}')

    with_properties = ['path_alias', 'original_format', 'o_dims', 'tags', 'url_k']
    params = self._get_photos_params(user, extra_params=with_properties)

    log.debug('URL: %s', Flickr.API_URL)
    log.debug('PARAMS: %s', params)
    response = requests.get(url=Flickr.API_URL, params=params)

    if response.status_code != 200:
      log.error('failed calling API: %s', response.text)
      return None

    json_response = response.json()

    if 'code' in json_response and json_response['code'] != 200:
      log.error('API returned error: %s', response.text)
      return None

    photos_response = json_response['photos']

    photos: dict[str, PhotoMeta] = {}

    for photo_response in photos_response['photo']:
      photos[photo_response['id']] = self._flickr_to_photo(photo_response)

    if photos_response['pages'] > 1:
      for i in range(2, photos_response['pages'] + 1):
        params['page'] = i
        response = requests.get(url=self.API_URL, params=params)
        json_response = response.json()
        photos_response = json_response['photos']

        for photo_response in photos_response['photo']:
          photos[photo_response['id']] = self._flickr_to_photo(photo_response)

    return photos

  def download_photo(self, photo_url: str, file_name: str) -> None:
    log.info(f'Downloading photo from Flickr: url={photo_url}, file={file_name}')

    with urllib.request.urlopen(photo_url) as response, open(file_name, 'wb') as out_file:
      shutil.copyfileobj(response, out_file)

  def _get_photos_params(self,
                         username: str,
                         safe_search=1,
                         min_upload_date='2020-12-01',
                         content_types=0,
                         privacy_filter=1,
                         per_page=500,
                         page=1,
                         extra_params=None) -> dict[str, Any]:
    extra_params = extra_params or []
    return {
      'method': 'flickr.people.getPhotos',
      'api_key': self._config.api_key,
      'user_id': username,
      'safe_search': safe_search,
      'min_upload_date': min_upload_date,
      'content_types': content_types,
      'privacy_filter': privacy_filter,
      'per_page': per_page,
      'page': page,
      'extras': ', '.join(extra_params),
      'format': 'json',
      'nojsoncallback': 1,
    }

  def _flickr_to_photo(self, flickr_photo: dict[str, Any]) -> PhotoMeta:
    tags = flickr_photo.get('tags', '')
    return {
      'id': flickr_photo.get('id'),
      'title': flickr_photo.get('title'),
      'is_public': True if flickr_photo.get('ispublic', False) == 1 else False,
      'original_width': flickr_photo.get('o_width'),
      'original_height': flickr_photo.get('o_height'),
      'original_format': flickr_photo.get('originalformat'),
      'tags': tags.split(),
      'url': flickr_photo.get('url_k'),
      'width': flickr_photo.get('width_k'),
      'height': flickr_photo.get('height_k'),
      'owner': flickr_photo.get('owner'),
      'owner_alias': flickr_photo.get('pathalias'),
      'pierrot_timestamp': str(datetime.now())
    }
