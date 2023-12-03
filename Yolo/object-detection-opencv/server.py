import socket, cv2, pickle, struct
import threading
import yolo_opencv
import traceback

def start_video_stream():
    print("Iniciando Camera listen port")
    global frame
    camera_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # camera_socket.connect((host_ip, port))
    host_ip = "127.0.0.1"
    port = 9997
    camera_address = (host_ip, port)
    camera_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    camera_socket.bind(camera_address)
    camera_socket.listen()
    print('Server listen to Camera - Listening at:', camera_address)
    while(True):
        camera_2_socket, addr = camera_socket.accept()
        try:
            print("Camera {} CONNECTED".format(addr))

            data = b""
            payload_size = struct.calcsize("Q")
            while True:
                while len(data) < payload_size:
                    packet = camera_2_socket.recv(4*1024)
                    if not packet: break
                    data+=packet
                packet_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packet_msg_size)[0]

                while len(data) < msg_size:
                    data+= camera_2_socket.recv(4*1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)
                # frame = yolo_opencv.image_analyzer(frame)
                # cv2.imshow("RECIEVING VIDEO", frame)
                # key = cv2.waitkey(1) & 0xFF
                # if key == ord('q'):
                #     break
        except Exception as e:
            print(f"Camera {addr} disconnected")
            traceback.print_exc()
            break
    camera_socket.close()

def serve_client():
    print("Iniciando Client listen port")
    global frame
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # camera_socket.connect((host_ip, port))
    host_ip = "127.0.0.1"
    port = 9999
    client_address = (host_ip, port)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.bind(client_address)
    client_socket.listen()
    print('Server listen to Client - Listening at:', client_address)
    while(True):
        client_2_socket, addr = client_socket.accept()
        try:
            print("Client {} CONNECTED".format(addr))
            if client_socket:
                while True:
                    frameClient = yolo_opencv.image_analyzer(frame)
                    # frameClient = frame
                    a = pickle.dumps(frameClient)
                    message = struct.pack("Q", len(a))+a
                    client_socket.sendall(message)

        except Exception as e:
            print(f"Client {addr} disconnected")
            traceback.print_exc()
            break
    client_socket.close()

global frame
frame = None

print("Iniciando Server")
thread = threading.Thread(target=start_video_stream, args=())
thread.start()
thread = threading.Thread(target=serve_client, args=())
thread.start()
print("Total clients ", threading.active_count()-2)