import socket
import numpy as np
import cv2


class UDPServer:
    BufferSize = 640 * 3

    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((host, port))
        self.sources = []
        self.frame = None

    def start(self, data_function: callable):
        while True:
            data, address = self.socket.recvfrom(UDPServer.BufferSize)
            if address in self.sources and len(data) == UDPServer.BufferSize:
                buffer = b''
                for x in range(480):
                    buffer += data
                if len(buffer) == 480 * 640 * 3:
                    frame = np.array(bytearray(buffer)).reshape((480, 640, 3))
                    data_function(frame)
                del buffer
            elif data == b'connect':
                print("Connected:", address)
                self.sources.append(address)
            elif data == b'close':
                print("Disconnected:", address)
                self.sources.remove(address)
                if len(self.sources) == 0:
                    break
        self.socket.close()


class UDPClient:
    BufferSize = 640 * 3

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.targets = []

    def connect(self, host, port):
        self.socket.sendto(b'connect', (host, port))
        self.targets.append((host, port))

    def disconnect(self, host, port):
        self.socket.sendto(b'close', (host, port))
        self.targets.remove((host, port))

    def sent_frame(self, frame):
        for address in self.targets:
            for x in range(480):
                self.socket.sendto(bytearray(np.array([x, frame[x]])), address)


if __name__ == '__main__':
    def show(frame):
        cv2.imshow('orginal', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return

    server = UDPServer("localhost", 10000)
    server.start(show)


# # Create a TCP/IP socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
# # Bind the socket to the port
# server_address = ('localhost', 10000)
# print(sys.stderr, 'starting up on %s port %s' % server_address)
# sock.bind(server_address)
# address = None
# while True:
#     # print(sys.stderr, '\nwaiting to receive message')
#     if address is None:
#         data, address = sock.recvfrom(0)
#     else:
#         # print(sys.stderr, 'received %s bytes from %s' % (len(data), address))
#         # print(sys.stderr, data)
#
#         # if data:
#         sent = sock.sendto(b'hello', address)
#         print(sys.stderr, 'sent %s bytes back to %s' % (sent, address))
