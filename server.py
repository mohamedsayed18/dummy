import asyncio
from asyncio import DatagramProtocol
from flask import Flask
import time, datetime
import json
import logging
import socket
import threading

class EchoServerProtocol(DatagramProtocol):

    def __init__(self):
        self.db = DB()
    
    def datagram_received(self, data, addr):
        if data:
            self.db.sensors[addr[1]] = [json.loads(data), time.time(),'UP']      

class DB:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not DB._instance:
            DB._instance = super(DB,cls).__new__(cls, *args, **kwargs)
        return DB._instance

    def __init__(self):
        self.sensors = {}
        self.status_update = {}

class Manipulator:

    def __init__(self, message):
        self.message = json.dumps(message)
        self.host = '127.0.0.1'
        self.port = 65432

    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(self.message.encode())

class WebApi:

    def __init__(self,db):

        self.api = Flask(__name__)
        self.db = db

    def run_api(self):

        @self.api.route('/sensors', methods=['GET'])
        def get_companies():

            sensors = self.db.sensors
            message = {}
            for i in sensors:
                message[i]={'datetime':sensors[i][0]['datetime'],
                            'status':sensors[i][2],
                            'time_of_decision':self.db.status_update[i]}

            return json.dumps(message)

        self.api.run(ssl_context='adhoc')



async def checker(db):

    while True:

        contr_list = db.sensors

        if contr_list:

            for i in contr_list:

                if time.time() - contr_list[i][1] >= 5 and contr_list[i][2] == 'UP':
                    contr_list[i][2] = 'DOWN'
                    logging.warning('Sensor {0} is DOWN'.format(i))
                else:
                    pass
            message = {}        
            for i in contr_list:
                logging.info(str(i) + ' ' + db.sensors[i][2])
                message[i]={'datetime':contr_list[i][0]['datetime'],
                            'status':contr_list[i][2]}

                db.status_update[i]=datetime.datetime.now().strftime("%Y-%m-%d-%H.%M:%S")
            
                
            manip = Manipulator(message)
            try:
                manip.connect()
            except ConnectionRefusedError:
                logging.warning('Manipulator is not available')
        else:
            logging.info('No sensors are found')

        await asyncio.sleep(5)

def controller(db):

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    task = loop.create_datagram_endpoint(protocol_factory=EchoServerProtocol,local_addr=('127.0.0.1', 6789))
    loop.create_task(checker(db))
    server = loop.run_until_complete(task)

    try:
        logging.info('Server started')
        loop.run_forever()
    except:
        loop.run_until_complete(server.wait_closed())
    finally:
        loop.close()

def web_api(db):

    wapi = WebApi(db)
    wapi.run_api()

def main():

    db = DB()

    thread_controller = threading.Thread(target=controller, args=(db,))
    thread_web_api = threading.Thread(target=web_api, args=(db,))
    thread_controller.start()
    thread_web_api.start()

if __name__ == '__main__': 
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    main()

