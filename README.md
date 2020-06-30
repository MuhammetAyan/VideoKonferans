# Video Konferans
Görüntülü konuşma programı

### Projede ilerlenen aşamalar
 - [X] Kameradan görüntü alma
 - [X] TCP ile frame gönderme
 - [X] UDP haberleşmesi sağlama
 - [ ] UDP ile karşıya frame gönderme
    > UDP paket yapısında maksimum gönderilebilecek data 65527 bayttır.
   Göndermek istediğim frame boyutu (yükseklik * boy * kanal sayısı) = 480 * 640 * 3 = 921600 olduğundan tek paket halinde gönderemem.
   921600 / 65527 = 14.0644 olduğundan minimum bir frame 15 UDP paketiyle gönderilebilir.
 - [ ] Tek UDP kanalı ile iki tarafın görüntüsünü birbirine gönderme
 - [ ] Ses verisini işleme
 - [ ] Ses verisini ayrı kanaldan karşıya gönderme
 - [ ] Ses verisini görüntü verisiyle aynı kanaldan gönderme
 
UDP Server, karşıdan gelen paketleri birleştirip görüntüleri oluşturur ve ekrana bastırır.
UDP Client ise kameradan aldığı görüntüyü karşıya gönderir.

### Temel uygulamalar
Projenin temelini oluşturan birkaç örnek proje aşağıda paylaşılmıştır.
#### Kameradan görüntü alma
```python
import numpy as np
import cv2
# Kameradan görüntü alma
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    # Eğer kameradan görüntü geliyorsa
    if ret:
        # Aynalamayı iptal ettik
        frame = cv2.flip(frame, 1)
        # Görüntüyü ekrana bastırdık.
        cv2.imshow('orginal', frame)
        # Görüntünün ekranda kalmasını sağladık.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()
```

#### UDP Server
```python
import socket
import sys
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print(sys.stderr, 'starting up on %s port %s' % server_address)
sock.bind(server_address)
address = None
while True:
    # print(sys.stderr, '\nwaiting to receive message')
    if address is None:
        data, address = sock.recvfrom(0)
    else:
        # print(sys.stderr, 'received %s bytes from %s' % (len(data), address))
        # print(sys.stderr, data)
        # if data:
        sent = sock.sendto(b'hello', address)
        print(sys.stderr, 'sent %s bytes back to %s' % (sent, address))
```

#### UDP Client
```python
import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)

try:
    # Send data
    # print(sys.stderr, 'sending "%s"' % message)
    sent = sock.sendto(b'', server_address)

    # Receive response
    # print(sys.stderr, 'waiting to receive')
    while True:
        data, server = sock.recvfrom(4096)
        print(sys.stderr, 'received "%s"' % data)
        sock.close()
        break
finally:
    print(sys.stderr, 'closing socket')
    sock.close()
```
