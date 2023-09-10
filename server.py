from socket import *
import sys

server_socket = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket
server_host = '' 
server_port = 80

server_socket.bind((server_host, server_port))
server_socket.listen(1)
print(f"Server is ready on {server_host}:{server_port}")

while True:
    print('Ready to serve...')
    connection_socket, addr = server_socket.accept()

    try:
        # Receive up to 1024 bytes of data from the client
        message = connection_socket.recv(1024).decode()

        if not message:
            continue

        filename = message.split()[1]

        # Send header and data from required file if exist
        try:
            f = open(filename[1:])
            output = f.read()
            f.close()
            response_headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
            connection_socket.send(response_headers.encode())

            for i in range(0, len(output)):
                connection_socket.send(output[i].encode())

            connection_socket.close()
            
        except:
            error_message = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\nFile Not Found"
            connection_socket.send(error_message.encode())
            connection_socket.close()

    except KeyboardInterrupt:
        break

server_socket.close()
sys.exit()
