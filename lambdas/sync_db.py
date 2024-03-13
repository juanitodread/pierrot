from pierrot.src.logging import get_logger


log = get_logger(__name__)


def do_work(event, context):
  log.info(f'Event: {event}')

  log.info('sync db function deployed')
