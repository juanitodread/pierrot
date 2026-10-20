from pierrot.src.clients.flickr.client import Flickr
from pierrot.src.clients.s3.client import S3
from pierrot.src.clients.twitter.client import TwitterFactory
from pierrot.src.clients.bluesky.client import BlueskyFactory
from pierrot.src.config import Config
from pierrot.src.logging import get_logger
from pierrot.src.pierrot import Pierrot


log = get_logger(__name__)


def do_work(event, context) -> None:
  log.info(f'Event: {event}, Context: {context}')

  flickr_config = Config.get_flickr_config()
  s3_config = Config.get_s3_config()
  twitter_config = Config.get_twitter_config()
  bluesky_config = Config.get_bluesky_config()

  flickr = Flickr(flickr_config)
  s3 = S3(s3_config)
  twitter = TwitterFactory.get_client(twitter_config)
  bluesky = BlueskyFactory.get_client(bluesky_config)

  pierrot = Pierrot(
    flickr_username=flickr_config.photos_owner,
    flickr=flickr,
    s3=s3,
    twitter=twitter,
    bluesky=bluesky,
  )
  pierrot.publish_photo()
