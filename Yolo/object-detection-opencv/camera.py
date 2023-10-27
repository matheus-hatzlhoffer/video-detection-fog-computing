import socket, cv2, pickle, struct
import imutils
import cv2

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host_name = socket.gethostname()
host_ip = "127.0.0.1"

print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)
server_socket.bind(socket_address)
server_socket.listen()
print('Listening at:', socket_address)

def start_video_stream():
    client_socket, addr = server_socket.accept()
    camera = False
    if camera == True:
        vid = cv2.VideoCapture(0)
    else:
        vid = cv2.VideoCapture("LondonBikeRideCityTour2022.mp4")
    try:
        print('Client {} CONNECTED!'.format(addr))
        if client_socket:
            while(vid.isOpened()):
                img, frame = vid.read()

                frame = imutils.resize(frame, width=320)
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a))+a
                client_socket.sendall(message)
                cv2.imshow("Transmitting to server", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    client_socket.close()
    except Exception as e:
        print(f"SERVER {addr} DISCONNECTED")
        pass

while(True):
    start_video_stream()
