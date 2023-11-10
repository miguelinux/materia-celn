#!/usr/bin/env python3
# vi: set shiftwidth=4 tabstop=8 expandtab:
import numpy as np
import cv2 as cv
import socket
import json

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 10000        # The port used by the server

while True:
    # Leemos la imagen
    imagen = cv.imread("zidane.jpg")

    b_json = bytearray()

    encode_param = [int(cv.IMWRITE_JPEG_QUALITY), 90]
    result, img_enc = cv.imencode('.jpg', imagen, encode_param)

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
            b_json += data

    print("ok:", len(b_json))
    el_json = json.loads( b_json.decode() )
    for objetos in el_json:
        for x, y in objetos.items():
          print(x, y)
        print("----------")

    cv.imshow("Local", imagen)

    if cv.waitKey(1) == 27:
        break

cv.destroyAllWindows()
