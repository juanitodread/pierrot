import json

import boto3

from pierrot.src.clients.s3.config import S3Config
from pierrot.src.logging import get_logger


log = get_logger(__name__)


class S3:
  _PIERROT_METADATA_DB = 'pierrot-meta.json'
  _PIERROT_PHOTOS_DB = 'pierrot-db.json'
  _PIERROT_WAL_DB = 'pierrot-wal.json'

  def __init__(self, config: S3Config) -> None:
    self._config = config
    self._s3 = boto3.resource('s3')

  def get_metadata_db(self) -> dict:
    return self._get_object(self._config.bucket, S3._PIERROT_METADATA_DB)

  def save_metadata_db(self, content: dict) -> None:
    self._put_object(self._config.bucket, S3._PIERROT_METADATA_DB, content)

  def get_photos_db(self) -> dict:
    return self._get_object(self._config.bucket, S3._PIERROT_PHOTOS_DB)

  def save_photos_db(self, content: dict) -> None:
    self._put_object(self._config.bucket, S3._PIERROT_PHOTOS_DB, content)

  def get_wal_db(self) -> dict:
    return self._get_object(self._config.bucket, S3._PIERROT_WAL_DB)

  def save_wal_db(self, content: dict) -> None:
    self._put_object(self._config.bucket, S3._PIERROT_WAL_DB, content)

  def _get_object(self, bucket: str, key: str) -> dict:
    log.info(f'Getting object: bucket={bucket}, key={key}')

    object = self._s3.Object(bucket, key)
    return json.loads(object.get()['Body'].read().decode('utf-8'))

  def _put_object(self, bucket: str, key: str, content: dict) -> None:
    log.info(f'Putting object: bucket={bucket}, key={key}, objects-length={len(content)}')

    object = self._s3.Object(bucket, key)
    object.put(Body=(bytes(json.dumps(content).encode('UTF-8'))))

class S3Local(S3):
  def __init__(self, config: S3Config) -> None:
    self._config = config

  def get_metadata_db(self) -> dict:
    return self._read_file(f'{self._config.bucket}{S3._PIERROT_METADATA_DB}')

  def save_metadata_db(self, content: dict) -> None:
    self._write_file(f'{self._config.bucket}{S3._PIERROT_METADATA_DB}', content=content)

  def get_photos_db(self) -> dict:
    return self._read_file(f'{self._config.bucket}{S3._PIERROT_PHOTOS_DB}')

  def save_photos_db(self, content: dict) -> None:
    self._write_file(f'{self._config.bucket}{S3._PIERROT_PHOTOS_DB}', content=content)

  def get_wal_db(self) -> dict:
    return self._read_file(f'{self._config.bucket}{S3._PIERROT_WAL_DB}')

  def save_wal_db(self, content: dict) -> None:
    self._write_file(f'{self._config.bucket}{S3._PIERROT_WAL_DB}', content=content)

  def _write_file(self, file_name: str, content: dict) -> None:
    with open(file_name, 'w', encoding='utf-8') as f:
      json.dump(content, f, ensure_ascii=False, indent=2)

  def _read_file(self, file_name: str) -> dict:
    with open(file_name, encoding='utf-8') as f:
      return json.load(f)
