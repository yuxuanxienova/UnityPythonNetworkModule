import socket

#Define the host and port
HOST = '127.0.0.1' # Standard loopback interface address (localhost)
PORT = 65432 # Port to listen on (non-privileged ports are > 1023)

#Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# AF_INET is the address family for IPv4, and SOCK_STREAM is the socket type for TCP

#Bind the socket to the address and port
server_socket.bind((HOST, PORT))

#Listen for incoming connections
server_socket.listen()

print(f"Server is listening on {HOST}:{PORT}")

while True:
    #Accept the connection
    client_socket,client_address = server_socket.accept()

    with client_socket:
        print(f"Connected by {client_address}")
        while True:
            # Receive data from the client
            data = client_socket.recv(1024)  # Buffer size is 1024 bytes
            if not data:
                break
            print(f"Received: {data.decode()}")
            
            # Optionally, send a response to the client
            client_socket.sendall(data)

    