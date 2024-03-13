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


class TestPierrot:

  def test_sync_db(self, flickr_mock, s3_mock, caplog):
    flickr_mock.get_photos_total.return_value = {'photos': 43}

    pierrot = Pierrot('flickr-username', flickr=flickr_mock, s3=s3_mock)

    pierrot.sync_db()

    assert 'Pierrot DB synced: photos=43' == [rec.message for rec in caplog.records][-1]

  def test_sync_db_when_db_is_synced(self, flickr_mock, s3_mock, caplog):
    flickr_mock.get_photos_total.return_value = {'photos': 43}
    s3_mock.get_metadata_db.return_value = {'photos': 43}

    pierrot = Pierrot('flickr-username', flickr=flickr_mock, s3=s3_mock)

    pierrot.sync_db()

    assert 'Pierrot DB is already synced. Sync is not required: photos=43' == [rec.message for rec in caplog.records][-1]

  def test_sync_db_when_flickr_get_total_photos_api_fail(self, flickr_mock, s3_mock, caplog):
    flickr_mock.get_photos_total.return_value = None

    pierrot = Pierrot('flickr-username', flickr=flickr_mock, s3=s3_mock)

    pierrot.sync_db()

    assert 'Failed getting total photos from Flickr' == [rec.message for rec in caplog.records][-1]

  def test_sync_db_when_flickr_get_photos_metadata_api_fail(self, flickr_mock, s3_mock, caplog):
    flickr_mock.get_photos_metadata.return_value = None

    pierrot = Pierrot('flickr-username', flickr=flickr_mock, s3=s3_mock)

    pierrot.sync_db()

    assert 'Failed getting photos metadata from Flickr' == [rec.message for rec in caplog.records][-1]

  def test_sync_db_when_s3_get_metadata_db_api_fail(self, flickr_mock, s3_mock, caplog):
    s3_mock.get_metadata_db.side_effect = PierrotExeception('s3-error')

    pierrot = Pierrot('flickr-username', flickr=flickr_mock, s3=s3_mock)

    pierrot.sync_db()

    assert "Failed getting metadata DB from S3: ('Pierrot error: ', 's3-error')" == [rec.message for rec in caplog.records][-1]

  def test_sync_db_when_s3_save_metadata_db_api_fail(self, flickr_mock, s3_mock, caplog):
    s3_mock.save_metadata_db.side_effect = PierrotExeception('s3-error')

    pierrot = Pierrot('flickr-username', flickr=flickr_mock, s3=s3_mock)

    pierrot.sync_db()

    assert "Failed updating DB in S3: ('Pierrot error: ', 's3-error')" == [rec.message for rec in caplog.records][-1]

  def test_sync_db_when_s3_save_photos_db_api_fail(self, flickr_mock, s3_mock, caplog):
    s3_mock.save_photos_db.side_effect = PierrotExeception('s3-error')

    pierrot = Pierrot('flickr-username', flickr=flickr_mock, s3=s3_mock)

    pierrot.sync_db()

    assert "Failed updating DB in S3: ('Pierrot error: ', 's3-error')" == [rec.message for rec in caplog.records][-1]
