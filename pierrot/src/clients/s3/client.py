import json

import boto3

from pierrot.src.clients.s3.config import S3Config


class S3:
  def __init__(self, config: S3Config) -> None:
    session = boto3.Session(profile_name='pierrot')
    self._config = config
    self._s3 = session.resource('s3')

  def get_metadata_db(self) -> dict:
    return self._get_object(self._config.bucket, 'pierrot-meta.json')

  def save_metadata_db(self, content: dict) -> None:
    self._put_object(self._config.bucket, 'pierrot-meta.json', content)

  def get_photos_db(self) -> dict:
    return self._get_object(self._config.bucket, 'pierrot-db.json')

  def save_photos_db(self, content: dict) -> None:
    self._put_object(self._config.bucket, 'pierrot-db.json', content)

  def get_wal_db(self) -> dict:
    return self._get_object(self._config.bucket, 'pierrot-wal.json')

  def save_wal_db(self, content: dict) -> None:
    self._put_object(self._config.bucket, 'pierrot-wal.json', content)

  def _get_object(self, bucket: str, key: str) -> dict:
    print(f'GETTING OBJECT: bucket={bucket}, key={key}')

    object = self._s3.Object(bucket, key)
    return json.loads(object.get()['Body'].read().decode('utf-8'))

  def _put_object(self, bucket: str, key: str, content: dict) -> None:
    print(f'PUTTING OBJECT: bucket={bucket}, key={key}, objects-length={len(content)}')

    object = self._s3.Object(bucket, key)
    object.put(Body=(bytes(json.dumps(content).encode('UTF-8'))))

class S3Local(S3):
  def __init__(self, config: S3Config) -> None:
    self._config = config

  def get_metadata_db(self) -> dict:
    return self._read_file(f'{self._config.bucket}pierrot-meta.json')

  def save_metadata_db(self, content: dict) -> None:
    self._write_file(f'{self._config.bucket}pierrot-meta.json', content=content)

  def get_photos_db(self) -> dict:
    return self._read_file(f'{self._config.bucket}pierrot-db.json')

  def save_photos_db(self, content: dict) -> None:
    self._write_file(f'{self._config.bucket}pierrot-db.json', content=content)

  def get_wal_db(self) -> dict:
    return self._read_file(f'{self._config.bucket}pierrot-wal.json')

  def save_wal_db(self, content: dict) -> None:
    self._write_file(f'{self._config.bucket}pierrot-wal.json', content=content)

  def _write_file(self, file_name: str, content: dict) -> None:
    with open(file_name, 'w', encoding='utf-8') as f:
      json.dump(content, f, ensure_ascii=False, indent=2)

  def _read_file(self, file_name: str) -> dict:
    with open(file_name, encoding='utf-8') as f:
      return json.load(f)
