#!/usr/bin/env python3
# vi: set shiftwidth=4 tabstop=8 expandtab:
import numpy as np
import cv2 as cv
import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 10000        # The port used by the server

camara = cv.VideoCapture(0)

if not camara.isOpened():
    print("No puedo abrir la camara")
    exit(1)

while True:
    # Leemos la imagen de la camara
    ret, imagen = camara.read()

    if not ret:
        print("No podemos capturar la imagen de la camara")
        break

    # Obtenemos height, width y depth
    h, w, d = imagen.shape

    b_imagen = bytearray()

    encode_param = [int(cv.IMWRITE_JPEG_QUALITY), 90]
    result, img_enc = cv.imencode('.jpg', imagen, encode_param)

    if not result:
        continue

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        # Enviamos los datos de la imagen
        s.sendall(img_enc.size.to_bytes(4,byteorder="little"))
        # Enviamos la imagen
        print("size:", img_enc.size)
        s.sendall(img_enc.tobytes())
        while True:
            data = s.recv(4096)
            if not data:
                break
            b_imagen += data

    print("ok:", len(b_imagen))

    h = int.from_bytes(b_imagen[:2],  byteorder="little")
    w = int.from_bytes(b_imagen[2:4], byteorder="little")

    gris = np.ndarray(shape=(h,w), dtype='uint8',
                      buffer=b_imagen, offset=4)
    
    cv.imshow("Camara", gris)

    if cv.waitKey(1) == 27:
        break

camara.release()
cv.destroyAllWindows()
