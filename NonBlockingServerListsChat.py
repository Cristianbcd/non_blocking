#sudo lsof -t -i:7
#sudo kill -9 PID
import socket
import select
#import types
import queue

HOST = '127.0.0.1'
PORT = 7

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setblocking(False)
server_socket.bind((HOST, PORT))
server_socket.listen()
print('listening on', (HOST, PORT))

potential_readers = [server_socket]
potential_writers = []
queues = {}


while True:
	ready_to_read, ready_to_write, in_error = select.select(potential_readers,potential_writers,potential_readers,1)
	for socket in ready_to_read:
		if socket is server_socket:
			new_client_socket, new_client_address = socket.accept()
			print('Accepted connection from: ', new_client_address)
			new_client_socket.setblocking(False)
			potential_readers.append(new_client_socket)
			queues[new_client_socket] = queue.Queue()
		else:
			try:
				data = socket.recv(1024)
				if data:
					print('Receiving data from: ', socket.getpeername()[0], ":" ,socket.getpeername()[1])
					message = data.decode("utf-8")
					print("Received >> ", message)
					if socket not in potential_writers:
						potential_writers.append(socket)
					for future_broadcast in potential_writers:
						queues[future_broadcast].put(message)
				else:
					print("Closing connection >> ", socket.getpeername()[0], ":" ,socket.getpeername()[1])
					if socket in potential_writers:
						potential_writers.remove(socket)
					potential_readers.remove(socket)
					socket.close()
					del queues[socket]
			except:
				print("Closing connection >> ", socket.getpeername()[0], ":" ,socket.getpeername()[1])
				if socket in potential_writers:
					potential_writers.remove(socket)
				potential_readers.remove(socket)
				socket.close()
				del queues[socket]
				break
	
	for socket in ready_to_write:
		if not socket._closed:
			if not queues[socket].empty():
				message = queues[socket].get_nowait()
				socket.sendall(bytes(message, 'utf-8'))