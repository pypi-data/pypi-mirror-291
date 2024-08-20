import faust

from .broker_settings import settings as broker_settings
from .client_settings import settings as client_settings

app = faust.App(
    client_settings.SERVICE_NAME,
    broker=broker_settings.URL,
    value_serializer='raw',
    web_host=client_settings.HOST,
    web_port=client_settings.IN_PORT,
    producer_max_request_size=2000000
)

vectorize_topic = app.topic(
    broker_settings.VECTORIZE_TOPIC,
    partitions=8,
    maxsize=1500000
)



