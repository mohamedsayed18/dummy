import socket
import logging
import json

HOST = '127.0.0.1'
PORT = 65432

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
                for i in data:
                    if data[i]['status'] == 'DOWN':
                        logging.warning(' Controller: '+i+' ' + data[i]['status'] + ' ' +data[i]['datetime'] )
                    else:
                        logging.info(' Controller: '+i+' ' + data[i]['status'] + ' ' +data[i]['datetime'] )