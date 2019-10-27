import socket
import logging
import json

HOST = '127.0.0.1'
PORT = 65432

c = (
    "\033[0m",   # End of color
    "\033[36m",  # Cyan
    "\033[91m",  # Red
    "\033[35m",  # Magenta
)



logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        with conn:

            while True:
                data = conn.recv(1024)
                if not data:
                    break
                else:
                    data = json.loads(data.decode())
                print(c[3]+'--------------------------------------------'+ c[0] )
                for i in data:
                    if data[i]['status'] == 'DOWN':
                        logging.warning(c[2]+' Controller: '+i+' ' + data[i]['status'] + ' ' +data[i]['datetime']+ c[0] )
                    else:
                        logging.info(c[1]+' Controller: '+i+' ' + data[i]['status'] + ' ' +data[i]['datetime'] +c[0] )