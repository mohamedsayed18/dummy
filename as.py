import socket
import json
import asyncio
import datetime, time

controllers = 8
status = {}
	
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

def updater(data,addr):
#	time.sleep(1)
	for i in range(0,100000):
		b = 1+1 
	

def main():
	a = 0
	while True:
		data, addr = serverSock.recvfrom(1024)
		if data:
			updater(data.decode(),addr)
			a = a + 1
			print ('Number of packets', a)

main()
