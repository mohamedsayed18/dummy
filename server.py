import asyncio
from asyncio import DatagramProtocol
import time
import json
import logging
import socket

class EchoServerProtocol(DatagramProtocol):

    def __init__(self):
        self.db = DB()
    
    def datagram_received(self, data, addr):
        if data:
            self.db.controllers[addr[1]] = [json.loads(data), time.time(),'UP']      

class DB:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not DB._instance:
            DB._instance = super(DB,cls).__new__(cls, *args, **kwargs)
        return DB._instance

    def __init__(self):
        self.controllers = {}  

class manipulator:

    def __init__(self, message):
        self.message = json.dumps(message)
        self.host = '127.0.0.1'
        self.port = 65432

    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(self.message.encode())

async def checker(db):

    while True:

        contr_list = db.controllers

        if contr_list:

            for i in contr_list:

                if time.time() - contr_list[i][1] >= 5 and contr_list[i][2] == 'UP':
                    contr_list[i][2] = 'DOWN'
                    logging.warning('Controller {0} is DOWN'.format(i))
                else:
                    pass
            message = {}        
            for i in contr_list:
                logging.info(str(i) + ' ' + db.controllers[i][2])
                message[i]={'datetime':contr_list[i][0]['datetime'],
                            'status':contr_list[i][2]}
            
                
            manip = manipulator(message)
            try:
                manip.connect()
            except ConnectionRefusedError:
                logging.warning('Manipulator is not available')
        else:
            logging.info('No controllers are found')

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
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    main()

