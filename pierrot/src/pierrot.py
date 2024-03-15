from datetime import datetime
import random

from pierrot.src.clients.flickr.client import Flickr
from pierrot.src.clients.s3.client import S3
from pierrot.src.clients.twitter.client import Twitter
from pierrot.src.errors import PierrotExeception
from pierrot.src.logging import get_logger


log = get_logger(__name__)


class Pierrot:
  def __init__(self, flickr_username: str, flickr: Flickr, s3: S3, twitter: Twitter) -> None:
    self._flickr_username = flickr_username
    self._flickr = flickr
    self._s3 = s3
    self._twitter = twitter

  def sync_db(self) -> None:
    log.info('Syncing Pierrot DB')

    total_photos_response = self._flickr.get_photos_total(self._flickr_username)
    if not total_photos_response:
      log.error('Failed getting total photos from Flickr')
      return

    try:
      metadata_db = self._s3.get_metadata_db()
    except PierrotExeception as error:
      log.error(f'Failed getting metadata DB from S3: {error}')
      return

    total_photos_flickr = total_photos_response['photos']
    total_photos_pierrot = metadata_db.get('photos', 0)

    if total_photos_pierrot == total_photos_flickr:
      log.info(f'Pierrot DB is already synced. Sync is not required: photos={total_photos_flickr}')
      return

    log.info(f'New {total_photos_flickr - total_photos_pierrot} photos found. Syincing Pierrot DB...')

    updated_photos_metadata = self._flickr.get_photos_metadata(self._flickr_username)
    if not updated_photos_metadata:
      log.error('Failed getting photos metadata from Flickr')
      return

    try:
      self._s3.save_metadata_db(total_photos_response)
      self._s3.save_photos_db(updated_photos_metadata)
    except PierrotExeception as error:
      log.error(f'Failed updating DB in S3: {error}')
      return

    log.info(f'Pierrot DB synced: photos={total_photos_flickr}')

  def publish_photo(self) -> None:
    log.info('Publishing a photo')

    try:
      photos_db = self._s3.get_photos_db()
      wal_photos_db = self._s3.get_wal_db()
    except PierrotExeception as error:
      log.error(f'Failed getting Pierrot DB from S3: {error}')
      return

    unpublished_photo_ids = [photo_id for photo_id in photos_db.keys()
                             if photo_id not in wal_photos_db]

    unpublished_photo_id = random.choice(unpublished_photo_ids)
    unpublished_photo = photos_db[unpublished_photo_id]
    unpublished_photo['pierrot_wal_timestamp'] = str(datetime.now())

    try:
      wal_photos_db[unpublished_photo['id']] = unpublished_photo
      self._s3.save_wal_db(wal_photos_db)
    except PierrotExeception as error:
      log.error(f'Failed storing WAL DB to S3: {error}')
      return

    try:
      photo_file_name = f'/tmp/photo.{unpublished_photo["original_format"]}'
      self._flickr.download_photo(unpublished_photo['url'], photo_file_name)
    except PierrotExeception as error:
      log.error('Failed downloading photo from Flickr is possible the file does not exist. '
                f'Photo metadata was stored in WAL to mark as published and discarded next time: {error}')
      return

    try:
      twitter_photo_id = self._twitter.upload_photo(photo_file_name)
      self._twitter.publish_tweet(twitter_photo_id, self._format_message(self._twitter._config.tweet_text))
    except PierrotExeception as error:
      log.error(f'Failed publishing photo to Twitter: {error}')
      return

    log.info(f'Photo published to Twitter: photo_url={unpublished_photo["url"]}')

  def _format_message(self, message: str) -> str:
    return message.replace('~', '\n')
