import io
import json

from botocore.stub import Stubber
from botocore.response import StreamingBody
import pytest

from pierrot.src.clients.s3.client import S3
from pierrot.src.clients.s3.config import S3Config


@pytest.fixture()
def pierrot_s3():
  return S3(S3Config('pierrot-db-test'))


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


class TestS3:
  def test_get_metadata_db(self, pierrot_s3):
    expected_message = self._s3_object_response({
      'photos': 2,
    })

    expected_params = {
      'Bucket': 'pierrot-db-test',
      'Key': 'pierrot-meta.json'
    }

    with Stubber(pierrot_s3._s3.meta.client) as s3_stub:
      s3_stub.add_response(
        method='get_object',
        service_response=expected_message,
        expected_params=expected_params,
      )

      meta_db = pierrot_s3.get_metadata_db()

      assert meta_db == {'photos': 2}

  def test_save_metadata_db(self, pierrot_s3):
    expected_params = {
      'Body': json.dumps({'photos': 2}).encode('utf-8'),
      'Bucket': 'pierrot-db-test',
      'Key': 'pierrot-meta.json'
    }

    with Stubber(pierrot_s3._s3.meta.client) as s3_stub:
      s3_stub.add_response(
        method='put_object',
        service_response={},
        expected_params=expected_params,
      )

      pierrot_s3.save_metadata_db({'photos': 2})

  def test_get_photos_db(self, pierrot_s3, photos_db_content):
    expected_message = self._s3_object_response(photos_db_content)

    expected_params = {
      'Bucket': 'pierrot-db-test',
      'Key': 'pierrot-db.json'
    }

    with Stubber(pierrot_s3._s3.meta.client) as s3_stub:
      s3_stub.add_response(
        method='get_object',
        service_response=expected_message,
        expected_params=expected_params,
      )

      meta_db = pierrot_s3.get_photos_db()

      assert meta_db == photos_db_content

  def test_save_photos_db(self, pierrot_s3, photos_db_content):
    expected_params = {
      'Body': json.dumps(photos_db_content).encode('utf-8'),
      'Bucket': 'pierrot-db-test',
      'Key': 'pierrot-db.json'
    }

    with Stubber(pierrot_s3._s3.meta.client) as s3_stub:
      s3_stub.add_response(
        method='put_object',
        service_response={},
        expected_params=expected_params,
      )

      pierrot_s3.save_photos_db(photos_db_content)

  def test_get_wal_db(self, pierrot_s3, photos_db_content):
    expected_message = self._s3_object_response(photos_db_content)

    expected_params = {
      'Bucket': 'pierrot-db-test',
      'Key': 'pierrot-wal.json'
    }

    with Stubber(pierrot_s3._s3.meta.client) as s3_stub:
      s3_stub.add_response(
        method='get_object',
        service_response=expected_message,
        expected_params=expected_params,
      )

      meta_db = pierrot_s3.get_wal_db()

      assert meta_db == photos_db_content

  def test_save_wal_db(self, pierrot_s3, photos_db_content):
    expected_params = {
      'Body': json.dumps(photos_db_content).encode('utf-8'),
      'Bucket': 'pierrot-db-test',
      'Key': 'pierrot-wal.json'
    }

    with Stubber(pierrot_s3._s3.meta.client) as s3_stub:
      s3_stub.add_response(
        method='put_object',
        service_response={},
        expected_params=expected_params,
      )

      pierrot_s3.save_wal_db(photos_db_content)

  def _s3_object_response(self, content: dict) -> dict:
    encoded_content = json.dumps(content).encode('utf-8')
    return {
      'Body': StreamingBody(
        io.BytesIO(encoded_content),
        len(encoded_content),
      )
    }
