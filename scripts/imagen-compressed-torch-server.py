#!/usr/bin/env python3
# vi: set shiftwidth=4 tabstop=8 expandtab:
import numpy as np
import cv2 as cv
import socket
import torch

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 10000        # Port to listen on (non-privileged ports are > 1023)

b_imagen = bytearray()

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        # Limpiamos el arreglo
        b_imagen.clear()
        with conn:
            # recivimos los primeros bytes
            data = conn.recv(4096)
            img_size = int.from_bytes(data[:4], byteorder="little")
            b_imagen += data[4:]
            print(f"Connected by {addr}, size:", img_size)
            while len(b_imagen) < img_size:
                data = conn.recv(4096)
                b_imagen += data
                print(len(b_imagen))
                if not data:
                    print("break")
                    break

            print("ok", len(b_imagen))

            # Los bytes los hacemos arreglo de numpy
            img_enc = np.ndarray(shape=(len(b_imagen),), dtype='uint8',
                                buffer=b_imagen, )

            # Convertimos la imagen JPG a imagen RAW
            color = cv.imdecode(img_enc, cv.IMREAD_COLOR)

            # Inference
            results = model(color)
            ret = results.pandas().xyxy[0].to_json(orient="records")
            conn.sendall(ret.encoded())
