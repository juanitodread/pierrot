from pierrot.src.clients.flickr.client import Flickr
from pierrot.src.clients.s3.client import S3


class Pierrot:
  def __init__(self, flickr_username, flickr: Flickr, s3: S3) -> None:
    self._flickr_username = flickr_username
    self._flickr = flickr
    self._s3 = s3

  def sync_db(self) -> None:
    total_photos_flickr = self._flickr.get_photos_total(self._flickr_username)
    total_photos_pierrot = self._s3.get_metadata_db()

    total_flickr = total_photos_flickr['photos']
    total_pierrot = total_photos_pierrot.get('photos', 0)
    
    if total_pierrot == total_flickr:
      print(f'DB is already synced. Sync is not required: photos={total_flickr}')
      return
    
    print(f'New {total_flickr - total_pierrot} photos found. Syncying DB...')
    updated_photos_metadata = self._flickr.get_photos_metadata(self._flickr_username)

    # This should be a transaction
    self._s3.save_metadata_db(total_photos_flickr)
    self._s3.save_photos_db(updated_photos_metadata)

    print(f'DB is now synced: photos_after={total_flickr}, photos_before={total_pierrot}')
  
  def publish_photo(self) -> None:
    import random
    photos = self._s3.get_photos_db()

    photo_id = random.choice(list(photos.keys()))
    random_photo = photos[photo_id]

    self._flickr.download_photo(random_photo['url'], f'tmp/photo.{random_photo["original_format"]}')
    pass

