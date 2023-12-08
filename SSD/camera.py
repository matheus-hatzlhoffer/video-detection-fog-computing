import socket, cv2, pickle, struct
import imutils
import cv2
import time


def start_video_stream():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    host_ip = "127.0.0.1"
    port = 9999
    socket_address = (host_ip, port)



    camera = False
    if camera == True:
        vid = cv2.VideoCapture(0)
    else:
        vid = cv2.VideoCapture("LondonBikeRideCityTour2022.mp4")
        # vid = cv2.VideoCapture("videoTeste.mp4")
    try:
        server_socket.connect(socket_address)
        print('Connected to server')
        while(vid.isOpened()):
            img, frame = vid.read()
            time.sleep(0.02)
            try:
                frame = imutils.resize(frame, width=640)
            except Exception as ex:
                print("End of Video")
                pass
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a))+a
            server_socket.sendall(message)
            cv2.imshow("Transmitting to server", frame)
            key = cv2.waitKey(1) & 0xFF
            # if key == ord('q'):
        server_socket.close()
    except Exception as e:
        print(f"COULDN'T CONECT TO SERVER, TRYING AGAIN")
        pass

while(True):
    start_video_stream()
