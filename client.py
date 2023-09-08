from socket import *
import sys


if len(sys.argv) != 4:
	print("Usage: python client.py <server_host> <server_port> <filename>")
	sys.exit(1)

server_host = sys.argv[1]
server_port = int(sys.argv[2])
filename = "/" + sys.argv[3]

try:
	client_socket = socket(AF_INET, SOCK_STREAM)

	# Connect to the server
	client_socket.connect((server_host, server_port))

	http_request = f"GET {filename} HTTP/1.1\r\n\r\n"

	# Send the request to the server
	client_socket.sendall(http_request.encode())

	# Receive and display the server's response
	response = b""
	while True:
		data = client_socket.recv(1024)
		if not data:
			break
		response += data

	print(response.decode())

except Exception as e:
	print(f"An error occurred: {e}")
finally:
	client_socket.close()
