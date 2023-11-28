import socket, cv2, pickle, struct
import threading
import yolo_opencv

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
# host_ip = "10.3.77.117"
# print('HOST IP:', host_ip)
host_ip = "127.0.0.1"
port = 9997
socket_address = (host_ip, port)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(socket_address)
server_socket.listen()
print('Listening at:', socket_address)

global frame
frame = None

def start_video_stream():
    global frame
    camera_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # camera_socket.connect((host_ip, port))
    host_ip = "127.0.0.1"
    port = 9999
    camera_address = (host_ip, port)
    camera_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    camera_socket.bind(camera_address)
    camera_socket.listen()
    while(True):
        client_2_socket, addr = camera_socket.accept()
        try:
            print("Client {} CONNECTED".format(addr))

            data = b""
            payload_size = struct.calcsize("Q")
            while True:
                while len(data) < payload_size:
                    packet = client_2_socket.recv(4*1024)
                    if not packet: break
                    data+=packet
                packet_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packet_msg_size)[0]

                while len(data) < msg_size:
                    data+= client_2_socket.recv(4*1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)
                # frame = yolo_opencv.image_analyzer(frame)
                # cv2.imshow("RECIEVING VIDEO", frame)
                # key = cv2.waitkey(1) & 0xFF
                # if key == ord('q'):
                #     break

            camera_socket.close()
        except Exception as e:
            print(f"Client {addr} disconnected")
            pass


thread = threading.Thread(target=start_video_stream, args=())
thread.start()

def serve_client(addr, client_socket):
    global frame
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
        pass

while True:
    client_socket, addr = server_socket.accept()
    print(addr)
    thread = threading.Thread(target=serve_client, args=(addr, client_socket))
    thread.start()
    print("Total clients ", threading.activeCount()-2)