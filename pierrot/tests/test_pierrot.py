import pytest

from unittest.mock import patch
from pierrot.src.errors import PierrotExeception
from pierrot.src.pierrot import Pierrot


@pytest.fixture()
@patch('pierrot.src.clients.flickr.client.Flickr')
def flickr_mock(flickr_mock):
  return flickr_mock


@pytest.fixture()
@patch('pierrot.src.clients.s3.client.S3')
def s3_mock(s3_mock):
  return s3_mock

@pytest.fixture()
@patch('pierrot.src.clients.twitter.client.Twitter')
def twitter_mock(twitter_mock):
  return twitter_mock


@pytest.fixture()
def photos_db_content():
  return {
    '53572261016': {
      'id': '53572261016',
      'title': 'DSC_5116',
      'is_public': True,
      'original_width': '3936',
      'original_height': '2624',
      'original_format': 'jpg',
      'tags': [
        'nikon',
        'nikonphotography',
        'd780'
      ],
      'url': 'https://live.staticflickr.com/f5813f242f_k.jpg',
      'width': 2048,
      'height': 1365,
      'owner': 'akira',
      'owner_alias': 'akira-toriyama',
      'pierrot_timestamp': '2024-03-11 17:48:30.291404'
    }
  }


class TestPierrot:

  def test_sync_db(self, flickr_mock, s3_mock, twitter_mock, caplog):
    flickr_mock.get_photos_total.return_value = {'photos': 43}

    pierrot = Pierrot(
      flickr_username='flickr-username',
      flickr=flickr_mock,
      s3=s3_mock,
      twitter=twitter_mock
    )

    pierrot.sync_db()

    assert 'Pierrot DB synced: photos=43' == [rec.message for rec in caplog.records][-1]

  def test_sync_db_when_db_is_synced(self, flickr_mock, s3_mock, twitter_mock, caplog):
    flickr_mock.get_photos_total.return_value = {'photos': 43}
    s3_mock.get_metadata_db.return_value = {'photos': 43}

    pierrot = Pierrot(
      flickr_username='flickr-username',
      flickr=flickr_mock,
      s3=s3_mock,
      twitter=twitter_mock
    )

    pierrot.sync_db()

    assert 'Pierrot DB is already synced. Sync is not required: photos=43' == [rec.message for rec in caplog.records][-1]

  def test_sync_db_when_flickr_get_total_photos_api_fail(self, flickr_mock, s3_mock, twitter_mock, caplog):
    flickr_mock.get_photos_total.return_value = None

    pierrot = Pierrot(
      flickr_username='flickr-username',
      flickr=flickr_mock,
      s3=s3_mock,
      twitter=twitter_mock
    )

    pierrot.sync_db()

    assert 'Failed getting total photos from Flickr' == [rec.message for rec in caplog.records][-1]

  def test_sync_db_when_flickr_get_photos_metadata_api_fail(self, flickr_mock, s3_mock, twitter_mock, caplog):
    flickr_mock.get_photos_metadata.return_value = None

    pierrot = Pierrot(
      flickr_username='flickr-username',
      flickr=flickr_mock,
      s3=s3_mock,
      twitter=twitter_mock
    )

    pierrot.sync_db()

    assert 'Failed getting photos metadata from Flickr' == [rec.message for rec in caplog.records][-1]

  def test_sync_db_when_s3_get_metadata_db_api_fail(self, flickr_mock, s3_mock, twitter_mock, caplog):
    s3_mock.get_metadata_db.side_effect = PierrotExeception('s3-error')

    pierrot = Pierrot(
      flickr_username='flickr-username',
      flickr=flickr_mock,
      s3=s3_mock,
      twitter=twitter_mock
    )

    pierrot.sync_db()

    assert "Failed getting metadata DB from S3: ('Pierrot error: ', 's3-error')" == [rec.message for rec in caplog.records][-1]

  def test_sync_db_when_s3_save_metadata_db_api_fail(self, flickr_mock, s3_mock, twitter_mock, caplog):
    s3_mock.save_metadata_db.side_effect = PierrotExeception('s3-error')

    pierrot = Pierrot(
      flickr_username='flickr-username',
      flickr=flickr_mock,
      s3=s3_mock,
      twitter=twitter_mock
    )

    pierrot.sync_db()

    assert "Failed updating DB in S3: ('Pierrot error: ', 's3-error')" == [rec.message for rec in caplog.records][-1]

  def test_sync_db_when_s3_save_photos_db_api_fail(self, flickr_mock, s3_mock, twitter_mock, caplog):
    s3_mock.save_photos_db.side_effect = PierrotExeception('s3-error')

    pierrot = Pierrot(
      flickr_username='flickr-username',
      flickr=flickr_mock,
      s3=s3_mock,
      twitter=twitter_mock
    )

    pierrot.sync_db()

    assert "Failed updating DB in S3: ('Pierrot error: ', 's3-error')" == [rec.message for rec in caplog.records][-1]

  def test_publish_photo(self, flickr_mock, s3_mock, twitter_mock, photos_db_content, caplog):
    s3_mock.get_photos_db.return_value = photos_db_content
    s3_mock.get_wal_db.return_value = {}

    pierrot = Pierrot(
      flickr_username='flickr-username',
      flickr=flickr_mock,
      s3=s3_mock,
      twitter=twitter_mock
    )

    pierrot.publish_photo()

    expected_log_message = [rec.message for rec in caplog.records][-1]
    assert 'Photo published to Twitter: photo_url=https://live.staticflickr.com/f5813f242f_k.jpg' == expected_log_message

  def test_publish_photo_when_s3_get_photos_db_fail(self, flickr_mock, s3_mock, twitter_mock, photos_db_content, caplog):
    s3_mock.get_photos_db.side_effect = PierrotExeception('s3-error')
    s3_mock.get_wal_db.return_value = {}

    pierrot = Pierrot(
      flickr_username='flickr-username',
      flickr=flickr_mock,
      s3=s3_mock,
      twitter=twitter_mock
    )

    pierrot.publish_photo()

    assert "Failed getting Pierrot DB from S3: ('Pierrot error: ', 's3-error')" == [rec.message for rec in caplog.records][-1]

  def test_publish_photo_when_s3_get_wal_db_fail(self, flickr_mock, s3_mock, twitter_mock, photos_db_content, caplog):
    s3_mock.get_photos_db.return_value = photos_db_content
    s3_mock.get_wal_db.side_effect = PierrotExeception('s3-error')

    pierrot = Pierrot(
      flickr_username='flickr-username',
      flickr=flickr_mock,
      s3=s3_mock,
      twitter=twitter_mock
    )

    pierrot.publish_photo()

    assert "Failed getting Pierrot DB from S3: ('Pierrot error: ', 's3-error')" == [rec.message for rec in caplog.records][-1]

  def test_publish_photo_when_s3_save_wal_db_fail(self, flickr_mock, s3_mock, twitter_mock, photos_db_content, caplog):
    s3_mock.get_photos_db.return_value = photos_db_content
    s3_mock.get_wal_db.return_value = {}
    s3_mock.save_wal_db.side_effect = PierrotExeception('s3-error')

    pierrot = Pierrot(
      flickr_username='flickr-username',
      flickr=flickr_mock,
      s3=s3_mock,
      twitter=twitter_mock
    )

    pierrot.publish_photo()

    assert "Failed storing WAL DB to S3: ('Pierrot error: ', 's3-error')" == [rec.message for rec in caplog.records][-1]

  def test_publish_photo_when_flickr_download_photo_fail(self, flickr_mock, s3_mock, twitter_mock, photos_db_content, caplog):
    s3_mock.get_photos_db.return_value = photos_db_content
    s3_mock.get_wal_db.return_value = {}
    flickr_mock.download_photo.side_effect = PierrotExeception('flickr-error')

    pierrot = Pierrot(
      flickr_username='flickr-username',
      flickr=flickr_mock,
      s3=s3_mock,
      twitter=twitter_mock
    )

    pierrot.publish_photo()

    assert "Failed downloading photo from Flickr is possible the file does not exist. "
    "Photo metadata was stored in WAL to mark as published and discarded next time: "
    "('Pierrot error: ', 'flickr-error')" == [rec.message for rec in caplog.records][-1]

  def test_publish_photo_when_twitter_upload_photo_fail(self, flickr_mock, s3_mock, twitter_mock, photos_db_content, caplog):
    s3_mock.get_photos_db.return_value = photos_db_content
    s3_mock.get_wal_db.return_value = {}
    twitter_mock.upload_photo.side_effect = PierrotExeception('twitter-error')

    pierrot = Pierrot(
      flickr_username='flickr-username',
      flickr=flickr_mock,
      s3=s3_mock,
      twitter=twitter_mock
    )

    pierrot.publish_photo()

    expected_message = [rec.message for rec in caplog.records][-1]
    assert "Failed publishing photo to Twitter: ('Pierrot error: ', 'twitter-error')" == expected_message

  def test_publish_photo_when_twitter_publish_tweet_fail(self, flickr_mock, s3_mock, twitter_mock, photos_db_content, caplog):
    s3_mock.get_photos_db.return_value = photos_db_content
    s3_mock.get_wal_db.return_value = {}
    twitter_mock.publish_tweet.side_effect = PierrotExeception('twitter-error')

    pierrot = Pierrot(
      flickr_username='flickr-username',
      flickr=flickr_mock,
      s3=s3_mock,
      twitter=twitter_mock
    )

    pierrot.publish_photo()

    expected_message = [rec.message for rec in caplog.records][-1]
    assert "Failed publishing photo to Twitter: ('Pierrot error: ', 'twitter-error')" == expected_message
