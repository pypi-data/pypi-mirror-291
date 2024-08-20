import asyncio
import logging
from typing import Callable, Any, Dict
from shared_kernel.interfaces import DataBus
from concurrent.futures import ThreadPoolExecutor
from shared_kernel.http import HttpClient

logging.getLogger().setLevel(logging.INFO)


class HTTPDatabus(DataBus):
    """
    A class to handle EventBridge and SQS operations.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(HTTPDatabus, cls).__new__(cls)
        return cls._instance

    def __init__(self, config: Dict = None):
        """
        Initialize the NATSInterface.

        Args:
            config (Dict): A Dict containing the NATS config.
        """
        if not hasattr(self, "initialized"):  # to prevent reinitialization
            super().__init__()
            self.http_client = HttpClient().create_client()

    async def publish_event(self, topic: str, event_payload: dict):
        """
        Sends an event payload to an HTTP endpoint and returns the response.

        :param topic: The URL for invoking the HTTP endpoint.
        :param event_payload: The payload containing all necessary information for invoking the HTTP endpoint.
        :return: The response from the HTTP endpoint.
        """

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.http_client.post, url=url, json=event_payload) for url in topic]
            for future in futures:
                future.result()

    def subscribe_async_event(self, topic: str, callback: Callable[[Any], None]):
        """
        Subscribes to synchronous events and invokes the provided callback upon receiving an event.

        :param callback: The callback function to invoke with the event data.
        """
        return asyncio.create_task(callback(topic))

    def request_event(self, topic: str, event_payload: dict) -> Any:
        """
        Sends an event payload to an HTTP endpoint and returns the response.

        :param topic: The URL for invoking the HTTP endpoint.
        :param event_payload: The payload containing all necessary information for invoking the HTTP endpoint.
        :return: The response from the HTTP endpoint.
        """
        response = self.http_client.post(url=topic, json=event_payload)
        return response

    def subscribe_sync_event(self, topic: str, callback: Callable[[Any], None]):
        """
        Subscribes to synchronous events and invokes the provided callback upon receiving an event.

        :param callback: The callback function to invoke with the event data.
        """
        return callback(topic)

    def delete_message(self, receipt_handle: str):
        pass

    def make_connection(self, receipt_handle: str):
        pass

    def close_connection(self, receipt_handle: str):
        pass