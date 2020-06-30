# VideoKonferans
Görüntülü konuşma programı

UDP Server, karşıdan gelen paketleri birleştirip görüntüleri oluşturur ve ekrana bastırır.
UDP Client ise kameradan aldığı görüntüyü karşıya gönderir.

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
