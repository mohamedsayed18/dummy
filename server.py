import socket
import json
import asyncio
import datetime, time


class EchoServerProtocol:

	def connection_made(self, transport):
		self.transport = transport

	def datagram_received(self, data, addr):
		time.sleep(1)
		message = data.decode()
		print('Received %r from %s' % (message, addr))



async def main():
	print('hello')
	loop = asyncio.get_event_loop()
	transport, protocol = await loop.create_datagram_endpoint(
		lambda: EchoServerProtocol(),
		local_addr=('127.0.0.1', 6789))
	await asyncio.sleep(1)
	print('world')
	await asyncio.sleep(3600)

asyncio.run(main())


