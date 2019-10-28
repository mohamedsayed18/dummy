from asyncio import DatagramProtocol
from flask import Flask, json

import asyncio, socket, threading
import time, datetime, logging
 
###To process UDP packets 
class ServerProtocol(DatagramProtocol):

    def __init__(self):
        self.db = DB()

    ###Update received data in db, tell server that sensors are live
    def datagram_received(self, data, addr):
        if data:
            self.db.sensors[addr[0]] = [json.loads(data), time.time(),'UP']  

###To store data from sensors
class DB:

    _instance = None

    ###Make singleton
    def __new__(cls, *args, **kwargs):
        if not DB._instance:
            DB._instance = super(DB,cls).__new__(cls, *args, **kwargs)
        return DB._instance

    ###Initate variables for storing data in dictionary format
    def __init__(self):
        self.sensors = {}
        self.status_update = {}

###Send data to Manipulator
class Manipulator:

    def __init__(self, message):
        self.message = json.dumps(message)
        self.host = 'manipulator'
        self.port = 65432

    ###TCP connection to the server
    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(self.message.encode())

###Running Flask web server
class WebApi:

    def __init__(self,db):

        self.api = Flask(__name__)
        self.db = db

    ### run server host 0.0.0.0 Port 5000 
    def run_api(self):

        ###API GET /senosts, return sensor, datetime, status, time of decision
        @self.api.route('/sensors', methods=['GET'])
        def get_sensors():

            sensors = self.db.sensors 
            message = {} 

            for i in sensors:
                message[i]={'datetime':sensors[i][0]['datetime'],
                            'status':sensors[i][2],
                            'time_of_decision':self.db.status_update[i]
                            }

            return json.dumps(message)

        self.api.run(host='0.0.0.0',ssl_context='adhoc',debug=False)


### coroutine checks every 5 second sensors status and sleep again 
async def checker(db):

    while True:

        sensor_list = db.sensors #takes list of sensors

        if sensor_list:

            for i in sensor_list:

                # if timer is not updated more than 5 seconds it becomes down
                if time.time() - sensor_list[i][1] >= 5 and sensor_list[i][2] == 'UP': 
                    sensor_list[i][2] = 'DOWN'
                    logging.warning(c[2]+'Sensor {0} is DOWN'.format(i)+c[0])
                else:
                    pass

            message = {} # preparing message to manipulator

            # message: sensor, datetime, status
            for i in sensor_list:
#                logging.info(str(i) + ' ' + db.sensors[i][2])
                message[i]={'datetime':sensor_list[i][0]['datetime'],
                            'status':sensor_list[i][2]}

                #update 
                db.status_update[i]=datetime.datetime.now().strftime("%Y-%m-%d-%H.%M:%S")
            
            # sending message to manipulator     
            manip = Manipulator(message)
            try:
                manip.connect()
            except ConnectionRefusedError:
                logging.warning(c[2]+'Manipulator is not available'+c[0])
        else:
            logging.info(c[2]+'No sensors are found'+c[0])

        await asyncio.sleep(5)#async sleep 5 seconds 

###Initiating async UDP SERVER host 0.0.0.0 port 6789
def controller(db):

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    task = loop.create_datagram_endpoint(protocol_factory=ServerProtocol,local_addr=('0.0.0.0', 6789))
    loop.create_task(checker(db)) # add task checker to event loop
    server = loop.run_until_complete(task) #add task udp server to event loop

    try:
        logging.info('Server started')
        loop.run_forever()
    except:
        loop.run_until_complete(server.wait_closed())
    finally:
        loop.close()

###Initatin WEB server
def web_api(db):

    wapi = WebApi(db)
    wapi.run_api()

### Main function to run two threads: UDP server and WEB server
def main():

    db = DB()

    thread_controller = threading.Thread(target=controller, args=(db,))
    thread_web_api = threading.Thread(target=web_api, args=(db,))
    thread_controller.start()
    thread_web_api.start()

if __name__ == '__main__':

    c = (
    "\033[0m",   # End of color
    "\033[36m",  # Cyan
    "\033[91m",  # Red
    "\033[35m",  # Magenta
    )

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    main()

