#!/usr/bin/env python3

import socket

HOST = 'httpbin.org'  # The server's hostname or IP address
PORT = 80        # The port used by the server

client = socket.socket()
client.connect((HOST, PORT))

#body = '{"key1":value1,"key2":value2}'

print("Request")
message = "GET /status/418 HTTP/1.0\r\n\r\n"
#message = message + "Content-Type:application/json\r\n"
#message = message + "Content-Length:" + str(len(body)) + "\r\n"
#message = message + "\r\n"
#message = message + body

print("\n" + message)

client.sendall(bytes(message, 'utf-8'))
data = client.recv(4096)
print("\n" + data.decode("utf-8"))
client.close()