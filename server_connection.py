import socket
import threading

class Server():
    client_list = []
    last_message = ""

    def __init__(self):
        self.server_socket = None
        self.listening_server()

    def listening_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        localhost_address = '127.0.0.1'
        localhost_port = 10319
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # this makes the server listen to requests coming from other computers on the network
        self.server_socket.bind((localhost_address, localhost_port))
        print("Waiting for incoming messages..")
        self.server_socket.listen(5)
        self.receive_messages_in_a_new_thread()

    def receive_messages(self,so):
        while True:
            incoming_message = so.recv(256)
            if not incoming_message:
                break
            self.last_message = incoming_message.decode('utf-8')
            self.send_to_all_clients(so)  # send to all clients
        so.close()

    def send_to_all_clients(self, senders_socket):
        for client in self.client_list:
            socket, (ip, port) = client
            if socket is not senders_socket:
                socket.sendall(self.last_message.encode('utf-8'))

    def receive_messages_in_a_new_thread(self):
        while True:
            client = so, (ip, port) = self.server_socket.accept()
            self.add_to_clients_list(client)
            print('Connected to ', ip, ':', str(port))
            t = threading.Thread(target=self.receive_messages, args=(so,))
            t.start()

    def add_to_clients_list(self, client):
        if client not in self.client_list:
            self.client_list.append(client)


if __name__ == "__main__":
    Server()