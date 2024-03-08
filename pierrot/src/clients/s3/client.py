import json


class S3:
  def get_metadata_db(self) -> dict:
    return {}
  
  def save_metadata_db(self, content: dict) -> None:
    pass

  def get_photos_db(self) -> dict:
    return {}
  
  def save_photos_db(self, content: dict) -> None:
    pass

class S3Local(S3):
  def get_metadata_db(self) -> dict:
    return self._read_file('tmp/pierrot-meta.json')
  
  def save_metadata_db(self, content: dict) -> None:
    self._write_file('tmp/pierrot-meta.json', content=content)

  def get_photos_db(self) -> dict:
    return self._read_file('tmp/pierrot-db.json')
  
  def save_photos_db(self, content: dict) -> None:
    self._write_file('tmp/pierrot-db.json', content=content)

  def _write_file(self, file_name: str, content: dict) -> None:
    with open(file_name, 'w', encoding='utf-8') as f:
      json.dump(content, f, ensure_ascii=False, indent=2)
  
  def _read_file(self, file_name: str) -> dict:
    with open(file_name, encoding='utf-8') as f:
      return json.load(f)
