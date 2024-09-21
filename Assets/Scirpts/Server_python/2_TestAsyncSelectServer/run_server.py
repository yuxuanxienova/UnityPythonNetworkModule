import socket
import select
import time
from typing import List, Dict

class ClientState:
    def __init__(self,client_socket:socket.socket):
        self.client_address = client_socket.getpeername()
        self.socket:socket.socket = client_socket
        self.readBuffer=None
        self.lastActiveTime = time.time()

class NetManager:
    def __init__(self):
        # Listening socket
        self.listen_fd:socket.socket = None
        # Dict to store all clients
        self.clientsDict:Dict[socket.socket,ClientState] = {}
        #Read list
        self.check_read = []
        #Ping interval
        self.ping_interval = 30

    def start_loop(self,listen_host:str, listen_port:int):
        #Create a socket object
        self.listen_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Bind the socket to the address and port
        self.listen_fd.bind((listen_host, listen_port))
        #Listen for incoming connections
        self.listen_fd.listen()
        print(f"Server is listening on {listen_host}:{listen_port}")

        while True:
            self.update_check_read()

            #Wait for an event on a readable socket
            readable, writable, exceptional = select.select(self.check_read, [], [], 1)# 1 means 1 second timeout

            for s in readable:
                pass

    def update_check_read(self):
        self.check_read = [self.listen_fd]
        for client in self.clientsDict.values():
            self.check_read.append(client.socket)

    def read_listen_fd(self):
        client_socket,client_address = self.listen_fd.accept()
        print(f"Connected by {client_address}")
        client_state = ClientState(client_socket)
        self.clientsDict[client_socket] = client_state

    def read_client_fd(self,client_socket:socket.socket):
        client_state = self.clientsDict[client_socket]



