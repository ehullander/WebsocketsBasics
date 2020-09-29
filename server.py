import argparse
import asyncio
import logging

import websockets
from websockets import WebSocketServerProtocol

logging.basicConfig(level=logging.INFO)


class Server:
    clients = set()

    async def register(self, websocket: WebSocketServerProtocol) -> None:
        self.clients.add(websocket)
        logging.info(f'Websocket on remote address {websocket.remote_address} is connected.')

    async def unregister(self, websocket: WebSocketServerProtocol) -> None:
        self.clients.remove(websocket)
        logging.info(f'Websocket on remote address {websocket.remote_address} is disconnected.')

    async def send_message_to_every_client(self, message_body: str) -> None:
        if self.clients:
            await asyncio.wait([client.send(message_body) for client in self.clients])

    async def ws_handler(self, websocket: WebSocketServerProtocol, uri: str) -> None:
        await self.register(websocket)
        try:
            await self.send_message_out(websocket)
        finally:
            await self.unregister(websocket)

    async def send_message_out(self, websocket: WebSocketServerProtocol) -> None:
        async for message_body in websocket:
            await self.send_message_to_every_client(message_body)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run an example producer.')
    parser.add_argument('-l', '--listen', default='localhost', help='Specify the IP address on which the server will start a websocket')
    parser.add_argument('-p', '--port', type=int, default=3000, help='Specify the port on which the server will start a websocket')
    args = parser.parse_args()

    server = Server()
    start_server = websockets.serve(server.ws_handler, args.listen, args.port)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()