#!/usr/bin/env python3

import socket
import threading

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 7        # The port used by the server

client = socket.socket()
client.connect((HOST, PORT))
print("Connected")

def worker():
	while True:
		try:
			message = client.recv(1024)
		except:
			print("CLOSED socket")
			break
			
		if message:
			print('\nReceived >> ', message.decode("utf-8"), '\n>> ', end='')
		else:
			print('CLOSED')
			break


th = threading.Thread(target=worker, args=())
th.start()

while True:
	message = input(">> ")
	if message == "exit":
		client.close()
		th.join()
		break
	client.sendall(bytes(message, 'utf-8'))
	#data = client.recv(1024)
	#print('Received >> ', data.decode("utf-8"))