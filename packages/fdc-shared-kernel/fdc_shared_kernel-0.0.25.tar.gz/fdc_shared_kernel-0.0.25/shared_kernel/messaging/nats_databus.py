import json
import logging
from nats.aio.client import Client as NATS
from nats.js.api import StreamConfig, ConsumerConfig, DeliverPolicy
from typing import Callable, Any, List, Union, Dict
from shared_kernel.interfaces import DataBus

logging.getLogger().setLevel(logging.INFO)


class NATSDataBus(DataBus):
    """
    A NATS Interface class to handle both standard NATS and JetStream operations.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(NATSDataBus, cls).__new__(cls)
        return cls._instance

    def __init__(self, config: Dict = None):
        """
        Initialize the NATSInterface.

        Args:
            config (Dict): A Dict containing the NATS config.
        """
        if not hasattr(self, "initialized"):  # to prevent reinitialization
            super().__init__()
            self.nc = NATS()
            self.servers = config.get('servers')
            self.user = config.get('user')
            self.password = config.get('password')
            self.connected = False
            self.js = None  # JetStream context
            self.initialized = True
            self.stream_name = config.get('stream_name', '')
            self.topics = config.get('topics', [])

            if self.stream_name:
                if self.topics:
                    self.create_stream(self.stream_name, self.topics)

    async def make_connection(self):
        """
        Connect to the NATS server.
        """
        if not self.connected:
            await self.nc.connect(servers=self.servers,
                                  user=self.user,
                                  password=self.password)
            self.js = self.nc.jetstream(timeout=10)
            self.connected = True

    async def close_connection(self):
        """
        Close the connection to the NATS server.
        """
        try:
            if self.connected:
                await self.nc.close()
                self.connected = False
        except Exception as e:
            raise e

    async def create_stream(self, stream_name: str, topics: List[Any]):
        """
        Create a stream for topics to persist the messages

        Args:
            topics (List): The messages in this topic with be persisted.
        """
        try:
            self.stream_name = stream_name
            # Check if the stream already exists
            await self.js.stream_info(stream_name)
            logging.info(f"Stream '{stream_name}' already exists.")
        except Exception:
            # Stream does not exist, so create it
            stream_config = StreamConfig(
                name=stream_name,
                subjects=topics,
                max_age=600,  # retain messages for 10 mins
            )
            await self.js.add_stream(stream_config)
            logging.info(f"Stream created :: {stream_name}")

    async def publish_event(
            self, topic: str, event_payload: dict
    ) -> Union[bool, Exception]:
        """
        Publish a message to a JetStream subject.

        Args:
            topic (str): The topic to publish the message to.
            event_payload (dict): The message to be published.

        Returns:
            bool: True if the event was published successfully.
        """
        ack = await self.js.publish(
            topic, json.dumps(event_payload).encode("utf-8")
        )
        logging.info(
            f"Published event '{event_payload.get('event_name')}' to topic '{topic}', ack: {ack}"
        )

    async def request_event(
            self, topic: str, event_payload: str, timeout: float = 10.0
    ) -> Union[dict, Exception]:
        """
        Send a request and wait for a response.

        Args:
            topic (str): The topic to publish the message to.
            event_payload (dict): The message to be published.
            timeout (float): The timeout for the request.

        Returns:
            dict: The response message.
        """
        response = await self.nc.request(
            topic, json.dumps(event_payload).encode("utf-8"), timeout=timeout
        )
        return json.loads(response.data.decode("utf-8"))

    async def subscribe_async_event(
            self, topic: str, callback: Callable[[Any], None], durable_name: str
    ):
        """
        Subscribe to a JetStream subject with a durable consumer and process messages asynchronously.

        Args:
            topic: The topic to subscribe to.
            callback: A callback function to handle received messages.
        """
        try:
            # Check if the consumer already exists
            await self.js.consumer_info(stream=self.stream_name, name=durable_name)
            logging.info(f"Consumer '{durable_name}' already exists.")
        except Exception:
            # Consumer does not exist, so create it
            self.consumer_config = ConsumerConfig(
                name=durable_name,
                durable_name=durable_name,
                deliver_policy=DeliverPolicy.ALL,
                deliver_subject=durable_name,
                max_deliver=1
            )
            await self.js.add_consumer(stream=self.stream_name, config=self.consumer_config)
            logging.info(f"Consumer '{durable_name}' created.")

        await self.js.subscribe_bind(stream=self.stream_name, cb=callback, config=self.consumer_config,
                                     consumer=durable_name)
        logging.info(f"Subscribed to async event on topic '{topic}'")

    async def subscribe_sync_event(self, topic: str, callback: Callable[[Any], None]):
        """
        Subscribe to a NATS subject and return a response after processing the message.

        Args:
            topic: The topic to subscribe to.
            callback: A callback function to handle received messages.
        """
        await self.nc.subscribe(topic, cb=callback)
        logging.info(f"Subscribed to sync event on topic '{topic}'")

    def delete_message(self, receipt_handle: str):
        pass

