"""Lambda handler."""
from aws_lambda_powertools.utilities.data_classes import event_source, S3Event
from aws_lambda_powertools.utilities.typing import LambdaContext


@event_source(data_class=S3Event)  # pylint: disable=no-value-for-parameter
def handler(event: S3Event, _context: LambdaContext) -> str:
    return f"Hello World! {event.bucket_name}"
