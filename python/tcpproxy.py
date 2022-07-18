import asyncio
import sys
import logging

server = "10.45.64.153"
port = 1234

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("TCPProxy")


class TCPProxy:

    def __init__(self, reader, writer):
        self._client_reader = reader
        self._client_writer = writer
        self._server_reader = None
        self._server_writer = None
        self._server_ip = server
        self._server_port = port

    async def connect_to_server(self):
        self._server_reader, self._server_writer = await asyncio.open_connection(
            self._server_ip, self._server_port)
        logger.debug("Connected to Server")

    async def client_to_server(self):
        while True:
            data = await self._client_reader.read(1024)
            if not data:
                break
            self._server_writer.write(data)
            await self._server_writer.drain()
        self._server_writer.close()

    async def server_to_client(self):
        while True:
            data = await self._server_reader.read(1024)
            if not data:
                break
            self._client_writer.write(data)
            await self._client_writer.drain()
        self._client_writer.close()

    async def run(self):
        await self.connect_to_server()
        c_to_s = asyncio.create_task(self.client_to_server())
        s_to_c = asyncio.create_task(self.server_to_client())
        await asyncio.gather(c_to_s, s_to_c)


class TCPListener:

    def __init__(self, ip, port):
        self._ip = ip
        self._port = port
        self._server = None

    async def _handle_client(self, reader, writer):
        proxy = TCPProxy(reader, writer)
        await proxy.run()

    async def run(self):
        self._server = await asyncio.start_server(self._handle_client,
                                                  self._ip, self._port)
        await self._server.serve_forever()


if __name__ == "__main__":
    ip1 = sys.argv[1]
    port1 = sys.argv[2]

    # start a TCP listener on ip1:port1
    listener = TCPListener(ip=ip1, port=port1)
    asyncio.run(listener.run(), debug=True)
