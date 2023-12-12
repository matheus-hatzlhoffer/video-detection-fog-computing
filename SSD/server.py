import socket, cv2, pickle, struct
import threading
# import yolo_opencv
import ssd
import time
import numpy as np

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
# host_ip = "10.3.77.117"
# print('HOST IP:', host_ip)
# host_ip = "127.0.0.1"
# host_ip = "192.168.0.131"
host_ip = "10.3.77.135"

port = 9997
socket_address = (host_ip, port)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(socket_address)
server_socket.listen()
print('Listening at:', socket_address)
global frame
global frame_ID
frame_ID = struct.pack("P",0)
frame = None

def start_video_stream():
    global frame
    global frame_ID
    camera_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # host_ip = "127.0.0.1"
    # host_ip = "192.168.0.131"
    host_ip = "10.3.77.135"
    port = 9999
    camera_address = (host_ip, port)

    camera_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    camera_socket.bind(camera_address)
    camera_socket.listen()

    while(True):
        camera_2_socket, addr = camera_socket.accept()
        try:
            print("Camera {} CONNECTED".format(addr))

            data = b""
            payload_size = struct.calcsize("Q")
            code_payload = struct.calcsize("P")
            while True:
                while len(data) < payload_size+code_payload:
                    packet = camera_2_socket.recv(4*1024)
                    if not packet: break
                    data+=packet
                packet_msg_size = data[:payload_size]
                frame_ID = data[payload_size:payload_size+code_payload]
                data = data[payload_size+code_payload:]
                msg_size = struct.unpack("Q", packet_msg_size)[0]
                while len(data) < msg_size:
                    data+= camera_2_socket.recv(4*1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)
                # frame = ssd.consulta_SSD(frame, net, CLASSES, COLORS)
                # frame = yolo_opencv.image_analyzer(frame)
                # cv2.imshow("RECIEVING VIDEO", frame)
                # key = cv2.waitkey(1) & 0xFF
                # if key == ord('q'):
                #     break

            camera_2_socket.close()
        except Exception as e:
            print(f"Camera {addr} disconnected")
            frame_ID = struct.pack("P",0)

            pass

thread = threading.Thread(target=start_video_stream, args=())
thread.start()

def serve_client(addr, client_socket):
    last_frame = struct.pack("P",0)
    global frame
    global frame_ID
    net, CLASSES, COLORS = ssd.load_model()
    try:
        print("Client {} CONNECTED".format(addr))
        if client_socket:
            frame_count = 0
            start_time = time.time()    
            while True:
                if last_frame != frame_ID:
                    try:
                        frameClient = ssd.consulta_SSD(frame, net, CLASSES, COLORS)
                    except Exception as ex:
                        frameClient = np.zeros(shape=[360, 640, 3], dtype=np.uint8) 
                    a = pickle.dumps(frameClient)
                    message = struct.pack("Q", len(a))+frame_ID+a
                    client_socket.sendall(message)
                    frame_count += 1

                    elapsed_time = time.time() - start_time

                    if elapsed_time > 1:
                        fps = frame_count / elapsed_time
                        print(f"FPS: {fps:.2f}")                    
                        frame_count = 0
                        start_time = time.time()
                    # last_frame = frame_ID
    except Exception as e:
        print(e)
        print(f"Client {addr} disconnected")
        pass

while True:
    client_socket, addr = server_socket.accept()
    print(addr)
    thread = threading.Thread(target=serve_client, args=(addr, client_socket))
    thread.start()
    print("Total clients ", threading.active_count()-2)