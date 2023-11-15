#!/usr/bin/env python3
# vi: set shiftwidth=4 tabstop=8 expandtab:
import numpy as np
import cv2 as cv
import socket
import json

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

    b_json = bytearray()

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
            b_json += data

    print("ok:", len(b_json))
    el_json = json.loads( b_json.decode() )
    for objetos in el_json:
        # Esquina Superior Izquierda
        esi = (int(objetos["xmin"]), int(objetos["ymin"]))
        # Esquina Inferior Derecha
        eid = (int(objetos["xmax"]), int(objetos["ymax"]))
        #confidence class name
        #for x, y in objetos.items():
        #  print(x, y)
        print(objetos["name"])
        print("----------")
        cv.rectangle(imagen,esi,eid, (255, 0, 0), 2)

    cv.imshow("Local", imagen)

    if cv.waitKey(1) == 27:
        break

cv.destroyAllWindows()
