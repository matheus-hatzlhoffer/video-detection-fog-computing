import socket
import cv2
import pickle
import struct
import imutils
import time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = "127.0.0.1"
port = 9999
socket_address = (host_ip, port)

def start_video_stream():
    camera = False

    if camera:
        vid = cv2.VideoCapture(0)
    else:
        vid = cv2.VideoCapture("LondonBikeRideCityTour2022.mp4")

    try:
        server_socket.connect(socket_address)
        print('Connected to server')

        while vid.isOpened():
            img, frame = vid.read()
            time.sleep(0.02)
            frame = imutils.resize(frame, width=320)
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            server_socket.sendall(message)
            cv2.imshow("Transmitting to server", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

    except Exception as e:
        print(f"Error: {e}")
    finally:
        server_socket.close()

start_video_stream()
