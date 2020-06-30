import socket
import sys
import numpy as np
import cv2
import threading


class T(threading.Thread):
    frame = None

    def t(self):
        while True:
            pass
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     continue


# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('192.168.1.110', 10000)
buffer_size = 640 * 480 * 3
sock.connect(server_address)
t1 = T()
t1.start()
try:
    while True:
        # Receive response
        data = sock.recv(buffer_size)
        if buffer_size == len(data):
            T.frame = np.array(bytearray(data)).reshape((480, 640, 3))
            cv2.imshow('orginal', T.frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
finally:
    print(sys.stderr, 'closing socket')
    sock.close()
    t1.join()
