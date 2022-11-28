"""Lambda handler."""
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import event_source, S3Event
from aws_lambda_powertools.utilities.typing import LambdaContext

from header_setter.s3file import S3File, InaccessibleFile

LOG = Logger()


@event_source(data_class=S3Event)  # pylint: disable=no-value-for-parameter
def handler(event: S3Event, _context: LambdaContext) -> str:
    """S3 Event Handler.

    Args:
        event (S3Event): S3 Event
        _context (LambdaContext): Lambda context

    Returns:
        str: Processing result
    """
    LOG.info(
        f"Received event to process following file: {event.bucket_name}/{event.object_key}"
    )
    result = process_event(event)
    LOG.info(result)
    return result


def process_event(event: S3Event) -> str:
    """Process event.

    Args:
        event (S3Event): S3 Event

    Returns:
        str: Processing result
    """
    file = S3File(event.bucket_name, event.object_key)
    try:
        if file.cache_control_configured:
            return f"File: {event.bucket_name}/{event.object_key} already has a cache control setting"
        file.configure_cache_control()
        return (
            f"Configured cache control on file: {event.bucket_name}/{event.object_key}"
        )
    except InaccessibleFile as err:
        return f"Unable to process file: {event.bucket_name}/{event.object_key}. Error: {err}"
