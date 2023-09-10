from socket import *
import threading
import time


# Function to handle an individual client's request
def handle_client(connection_socket):

    # set a delay to test with multiple requests 
    time.sleep(4)
    try:
        # Receive up to 1024 bytes of data from the client
        message = connection_socket.recv(1024).decode()

        if not message:
            return

        filename = message.split()[1]

        # Send header and data from the required file if it exists
        try:
            f = open(filename[1:])
            output = f.read()
            f.close()

            # Prepare and send HTTP response headers
            response_headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
            connection_socket.send(response_headers.encode())

            for i in range(0, len(output)):
                connection_socket.send(output[i].encode())

        except:
            error_message = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\nFile Not Found"
            connection_socket.send(error_message.encode())
        
    finally:
        connection_socket.close()



# Create a socket for the server
server_socket = socket(AF_INET, SOCK_STREAM)

# Configure server settings
server_host = ''
server_port = 80
server_socket.bind((server_host, server_port))

# Listen for incoming connections, allowing a maximum of 1 pending connection
server_socket.listen(1)
print(f"Server is ready on {server_host}:{server_port}")

while True:
    print('Ready to serve...')
    connection_socket, addr = server_socket.accept()

    client_thread = threading.Thread(target=handle_client, args=(connection_socket,))
    client_thread.start()
