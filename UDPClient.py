# import socket
# import sys
#
#
# # Create a UDP socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
# server_address = ('localhost', 10000)
#
# try:
#     # Send data
#     # print(sys.stderr, 'sending "%s"' % message)
#     sent = sock.sendto(b'', server_address)
#
#     # Receive response
#     # print(sys.stderr, 'waiting to receive')
#     while True:
#         data, server = sock.recvfrom(4096)
#         print(sys.stderr, 'received "%s"' % data)
#         sock.close()
#         break
# finally:
#     print(sys.stderr, 'closing socket')
#     sock.close()
import UDP
import cv2
import time
cap = cv2.VideoCapture(0)
client = UDP.UDPClient()

while True:
    try:
        print("Bağlantı deneniyor...")
        client.connect("localhost", 10000)
        print("Bağlantı başarılı.")
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                client.sent_frame(frame)
            else:
                break
        client.disconnect("localhost", 10000)
    except Exception as e:
        print(f"Başarısız oldu: '{str(e)}' 10 sn sonra tekrar denenecek.")
        time.sleep(10)


cap.release()
out.release()
cv2.destroyAllWindows()
