import socket

HOST = "192.168.1.10"
PORT = 21        

client = socket.socket()
client.connect((HOST, PORT))

client_port_number = client.getsockname()[1]
client_ip_address = client.getsockname()[0]

print("The client IP address and port number: {} {}".format(client_ip_address,client_port_number))

print(client.recv(4098).decode("utf-8"))

message = "USER cristian\r\n"

print("\n" + message + "\n");

client.sendall(bytes(message, 'utf-8'))

print(client.recv(4098).decode("utf-8"))

message = "PASS hiddenpassword\r\n"

print("\n" + message + "\n");

client.sendall(bytes(message, 'utf-8'))

print(client.recv(4098).decode("utf-8"))

message = "TYPE I\r\n"

print("\n" + message + "\n");

client.sendall(bytes(message, 'utf-8'))

print(client.recv(4098).decode("utf-8"))

listen_port = 39851
receive_response_socket = socket.socket()
receive_response_socket.bind((client_ip_address,listen_port));

ftp_ip = str(client_ip_address).replace(".",",")
ftp_port = str(int("{0:x}".format(listen_port)[:2], 16)) + "," + str(int("{0:x}".format(listen_port)[2:],16))

message = "PORT " + ftp_ip + "," + ftp_port +"\r\n"

print("\n" + message + "\n");

client.sendall(bytes(message, 'utf-8'))

print(client.recv(4098).decode("utf-8"))

message = 'LIST\r\n'

print("\n" + message + "\n");

client.sendall(bytes(message, 'utf-8'))
receive_response_socket.listen()
print(receive_response_socket.accept()[0].recv(4098).decode("utf-8"))

receive_response_socket.close()

message = "QUIT\r\n"

print("\n" + message + "\n");

client.sendall(bytes(message, 'utf-8'))

print(client.recv(4098).decode("utf-8"))

client.close();