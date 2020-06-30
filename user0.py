import socket
import sys
import numpy as np
import cv2

cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('', 10000)
print(sys.stderr, 'starting up on %s port %s' % server_address)
sock.bind(server_address)
sock.listen(1)
while True:
    connection, client_address = sock.accept()
    print("connected:", client_address)
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                connection.send(frame)
                print(".", sep="")
            else:
                break
    except:
        pass
    # data, address = sock.recvfrom(4096)

    # print(sys.stderr, 'received %s bytes from %s' % (len(data), address))
    # print(sys.stderr, data)
    #
    # if data:
    #     sent = sock.sendto(data, address)
    #     print(sys.stderr, 'sent %s bytes back to %s' % (sent, address))


cap.release()
out.release()
cv2.destroyAllWindows()
