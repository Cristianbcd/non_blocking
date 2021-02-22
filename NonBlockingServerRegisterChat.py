#sudo lsof -t -i:7
#sudo kill -9 PID
import socket
import selectors
import types
import queue

HOST = '127.0.0.1'
PORT = 7

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setblocking(False)
server_socket.bind((HOST, PORT))
server_socket.listen()
print('listening on', (HOST, PORT))

selector = selectors.DefaultSelector()
selector.register(server_socket, selectors.EVENT_READ, data=None)

while True:
	events = selector.select(timeout=None)
	for socket_key, event in events:
		if socket_key.data is None:
			new_client_socket, new_client_address = socket_key.fileobj.accept()
			print('Accepted connection from: ', new_client_address)
			new_client_socket.setblocking(False)
			data = types.SimpleNamespace(addr=new_client_address, queue=queue.Queue())
			events = selectors.EVENT_READ | selectors.EVENT_WRITE
			selector.register(new_client_socket, events, data=data) 
		else:
			if event & selectors.EVENT_READ:
				try:
					data = socket_key.fileobj.recv(1024)
					if data:
						print('Receiving data from: ', socket_key.fileobj.getpeername()[0], ":" ,socket_key.fileobj.getpeername()[1])
						message = data.decode("utf-8")
						print("Received >> ", message)
						for number, future_broadcast in selector.get_map().items():
							if future_broadcast.data:
								future_broadcast.data.queue.put_nowait(message)
					else:
						print("Closing connection >> ", socket_key.fileobj.getpeername()[0], ":" ,socket_key.fileobj.getpeername()[1])
						selector.unregister(socket_key.fileobj)
						socket_key.fileobj.close()
				except:
					print("Closing connection >> ", socket_key.fileobj.getpeername()[0], ":" ,socket_key.fileobj.getpeername()[1])
					selector.unregister(socket_key.fileobj)
					socket_key.fileobj.close()
			elif event & selectors.EVENT_WRITE:
					if not socket_key.data.queue.empty():
						message = socket_key.data.queue.get_nowait()
						#print("Sending >> ", message)
						socket_key.fileobj.sendall(bytes(message, 'utf-8'))