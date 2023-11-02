#!/usr/bin/env python3
# vi: set shiftwidth=4 tabstop=8 expandtab:
import numpy as np
import cv2 as cv
import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 10000        # Port to listen on (non-privileged ports are > 1023)

b_imagen = bytearray()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        # Limpiamos el arreglo
        b_imagen.clear()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(4096)

                b_imagen += data
                # Leemos los datos de with, height y deep
                h = int.from_bytes(b_imagen[:2],  byteorder="little")
                w = int.from_bytes(b_imagen[2:4], byteorder="little")
                d = int.from_bytes(b_imagen[4:6], byteorder="little")

                img_len = h*w*d

                if img_len > 0 and len(b_imagen) > img_len:
                    break

            color = np.ndarray(shape=(h,w,d), dtype='uint8',
                                buffer=b_imagen, offset=6)

            gris = cv.cvtColor(color, cv.COLOR_BGR2GRAY)

            h, w = gris.shape 

            conn.sendall(h.to_bytes(2,byteorder="little"))
            conn.sendall(w.to_bytes(2,byteorder="little"))
            conn.sendall(gris.tobytes())
