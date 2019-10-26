import asyncio
from asyncio import DatagramProtocol


class EchoServerProtocol(DatagramProtocol):

    def datagram_received(self, data, addr):
        loop = asyncio.get_event_loop()
        loop.create_task(self.handle_income_packet(data, addr))

    async def handle_income_packet(self, data, addr):
    # echo back the message, but 2 seconds later     
        print(data)
        await asyncio.sleep(2)
        print ('Hello')


def main():

  loop = asyncio.get_event_loop()
  task = loop.create_datagram_endpoint(protocol_factory=EchoServerProtocol,local_addr=('127.0.0.1', 6789))
  server = loop.run_until_complete(task)

  try:
    print('server started')
    loop.run_forever()
  except:
    loop.run_until_complete(server.wait_closed())
  finally:
    loop.close()


if __name__ == '__main__':
  main()

