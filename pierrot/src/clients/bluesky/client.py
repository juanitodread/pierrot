import re

from atproto import Client, models, client_utils

from pierrot.src.clients.bluesky.config import BlueskyConfig
from pierrot.src.errors import PierrotException
from pierrot.src.logging import get_logger


log = get_logger(__name__)


class Bluesky:
  def __init__(self, config: BlueskyConfig) -> None:
    self._client = Client()
    self._client.login(config.username, config.password)
    log.info('Bluesky Client created!')

  def publish_post(self, image_path: str, text: str) -> None:
    try:
      with open(image_path, 'rb') as f:
        img_data = f.read()

      aspect_ratio = models.AppBskyEmbedDefs.AspectRatio(height=3, width=4)

      self._client.send_image(text=self._parse_text_to_builder(text),
                              image=img_data,
                              image_alt='',
                              image_aspect_ratio=aspect_ratio)

      log.info(f'Post sent: {image_path=}, {text=}')
    except Exception as error:
      raise PierrotException(error)

  def _parse_text_to_builder(self, text: str) -> client_utils.TextBuilder:
    builder = client_utils.TextBuilder()
    pattern = r'(#[\wáéíóúÁÉÍÓÚñÑ]+)'

    tokens = re.split(pattern, text)

    for token in tokens:
      if not token:
        continue
      if token.startswith('#'):
        hashtag = token[1:]
        builder.tag(token, hashtag)
      else:
        builder.text(token)

    return builder


class BlueskyLocal(Bluesky):
  def __init__(self, config: BlueskyConfig) -> None:
    self._client = None
    log.info('Bluesky Mock client created!')

  def publish_post(self, image_path: str, text: str) -> None:
    log.info(f'Post sent: {image_path=}, {text=}')


class BlueskyFactory:
  @staticmethod
  def get_client(config: BlueskyConfig) -> Bluesky:
    if config.use_mock:
      return BlueskyLocal(config)
    else:
      return Bluesky(config)
