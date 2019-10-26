import socket
import datetime, time
import random
import json

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789

id_controller = 1

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s = time.perf_counter()

for i in range(0,1000):

#	payload = random.randint(1,1000)

#	if payload == 483000:
#		print ('I`m dead...')
#		time.sleep(20)

#	else:

	Message = {'datetime':datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S"),
#				'payload':payload,
				'id_controller':id_controller}

	clientSock.sendto(json.dumps(Message).encode(), (UDP_IP_ADDRESS, UDP_PORT_NO))
	time.sleep(1/300)

elapsed = time.perf_counter() - s
print(f"{__file__} executed in {elapsed:0.2f} seconds.")