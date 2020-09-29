import argparse
import asyncio
import logging

import websockets
from websockets.client import WebSocketClientProtocol

logging.basicConfig(level=logging.INFO)


async def consumer_handler(websocket: WebSocketClientProtocol) -> None:
    async for message in websocket:
        log_message(message)


async def consume(hostname: str, port: int) -> None:
    websocket_resource_url = f"ws://{hostname}:{port}"
    async with websockets.connect(websocket_resource_url) as websocket:
        await consumer_handler(websocket)


def log_message(message: str) -> None:
    logging.info(f"> {message}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run an example consumer.')
    parser.add_argument('-l', '--listen', type=str, default='localhost', help='Specify the IP address on which the consumer listens.')
    parser.add_argument('-p', '--port', type=int, default=3000, help='Specify the port on which the consumer listens.')
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume(hostname=args.listen, port=args.port))
    loop.run_forever()