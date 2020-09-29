
import argparse
import asyncio

import websockets


async def produce(message: str, host: str, port: int) -> None:
    async with websockets.connect(f"ws://{host}:{port}") as websocket:
        await websocket.send(message)
        await websocket.recv()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run an example producer.')
    parser.add_argument('-l', '--listen', type=str, default='localhost', help='Specify the IP address on which the producer will connect.')
    parser.add_argument('-p', '--port', type=int, default=3000, help='Specify the port on which the producer will connect.')
    parser.add_argument('-m', '--message', type=str, default="{}", help='Specify a json message.')
    args = parser.parse_args()

    asyncio.run(produce(message=args.message, host=args.listen, port=args.port))