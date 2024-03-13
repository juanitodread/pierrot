from pierrot.src.clients.flickr.client import Flickr
from pierrot.src.clients.s3.client import S3
from pierrot.src.logging import get_logger


log = get_logger(__name__)


class Pierrot:
  def __init__(self, flickr_username: str, flickr: Flickr, s3: S3) -> None:
    self._flickr_username = flickr_username
    self._flickr = flickr
    self._s3 = s3

  def sync_db(self) -> None:
    log.info('Syncing Pierrot DB')

    total_photos_response = self._flickr.get_photos_total(self._flickr_username)
    if not total_photos_response:
      log.error('Failed getting total photos from Flickr')
      return None

    metadata_db = self._s3.get_metadata_db()

    total_photos_flickr = total_photos_response['photos']
    total_photos_pierrot = metadata_db.get('photos', 0)

    if total_photos_pierrot == total_photos_flickr:
      log.info(f'Pierrot DB is already synced. Sync is not required: photos={total_photos_flickr}')
      return None

    log.info(f'New {total_photos_flickr - total_photos_pierrot} photos found. Syincing Pierrot DB...')

    updated_photos_metadata = self._flickr.get_photos_metadata(self._flickr_username)
    if not updated_photos_metadata:
      log.error('Failed getting photos metadata from Flickr')
      return None

    self._s3.save_metadata_db(total_photos_response)
    self._s3.save_photos_db(updated_photos_metadata)

    log.info(f'Pierrot DB synced: photos={total_photos_flickr}')
