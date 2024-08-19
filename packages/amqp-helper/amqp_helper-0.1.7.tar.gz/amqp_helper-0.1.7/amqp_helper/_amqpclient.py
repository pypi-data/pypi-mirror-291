"""This class is a modified Version of the aio_pika RabbitMQ Tutorial about RPC.

we modified the calls function so it takes a routing key so we can actualy call multiple functions.
original source can be found here:
https://aio-pika.readthedocs.io/en/latest/rabbitmq-tutorial/6-rpc.html

"""

import uuid
import json
import asyncio

from typing import MutableMapping, Optional, Union
from aio_pika import Message, connect_robust
from aio_pika.abc import (
    AbstractChannel,
    AbstractConnection,
    AbstractIncomingMessage,
    AbstractQueue,
)

from amqp_helper import AMQPConfig

TimeoutType = Optional[Union[int, float]]


class AMQPClient:
    connection: AbstractConnection
    channel: AbstractChannel
    callback_queue: AbstractQueue
    loop: asyncio.AbstractEventLoop

    def __init__(self, eventloop: Optional[asyncio.AbstractEventLoop] = None) -> None:
        self.futures: MutableMapping[str, asyncio.Future] = {}
        self.loop = eventloop or asyncio.get_running_loop()

    async def connect(self, amqp_config: AMQPConfig) -> "AMQPClient":
        self.connection = await connect_robust(**amqp_config.aio_pika(), loop=self.loop)
        self.channel = await self.connection.channel()
        self.callback_queue = await self.channel.declare_queue(
            exclusive=True, timeout=5
        )
        await self.callback_queue.consume(self.on_response, no_ack=True)

        return self

    async def close(self):
        """Function to close the AMQP Connection

        Returns:
            None
        """
        await self.connection.close()

    def on_response(self, message: AbstractIncomingMessage) -> None:
        """Functionhandler for an incoming message

        Args:
            message (AbstractIncomingMessage): The Incoming Message

        Returns:
            None
        """
        if message.correlation_id is None:
            print(f"Bad message {message!r}")
            return None
        future: asyncio.Future = self.futures.pop(message.correlation_id)
        future.set_result(json.loads(message.body))

    async def call(
        self, data: dict, routing_key: str, timeout: TimeoutType = 10
    ) -> dict:
        correlation_id = str(uuid.uuid4())
        future = self.loop.create_future()

        self.futures[correlation_id] = future

        message = Message(
            json.dumps(data).encode(),
            content_type="text/json",
            content_encoding="utf-8",
            correlation_id=correlation_id,
            reply_to=self.callback_queue.name,
            expiration=timeout,
        )

        await self.channel.default_exchange.publish(
            message, routing_key=routing_key, mandatory=True, timeout=timeout
        )

        returned_data = {}
        try:
            returned_data = await asyncio.wait_for(future, timeout)
        except asyncio.TimeoutError as exc:
            self.futures.pop(correlation_id)
            raise exc
        
        return returned_data
