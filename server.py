import asyncio
from asyncio import DatagramProtocol
import time
import json


class EchoServerProtocol(DatagramProtocol):

    def __init__(self):
        self.db = DB()
    
    def datagram_received(self, data, addr):

        loop = asyncio.get_event_loop()
        loop.create_task(self.handle_income_packet(data, addr))

    async def handle_income_packet(self, data,addr):
        
        self.db.controllers[addr] = [data, time.time(),'up']

class DB:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not DB._instance:
            DB._instance = super(DB,cls).__new__(cls, *args, **kwargs)
        return DB._instance

    def __init__(self):
        self.controllers = {}  


async def checker(db):

    while True:
        contr_list = db.controllers
        if contr_list:
            for i in contr_list:

                if time.time() - contr_list[i][1] >= 5 and contr_list[i][2] == 'up':
                    contr_list[i][2] = 'down'
                    print('Controller {0} is down'.format(i))
                else:
                    pass
        else:
            print('No controllers are founded')
        print (db.controllers) 
        await asyncio.sleep(5)

def main():
  db = DB()
  loop = asyncio.get_event_loop()
  task = loop.create_datagram_endpoint(protocol_factory=EchoServerProtocol,local_addr=('127.0.0.1', 6789))
  loop.create_task(checker(db))
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

