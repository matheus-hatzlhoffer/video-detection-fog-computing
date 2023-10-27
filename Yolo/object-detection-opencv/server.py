import socket, cv2, pickle, struct
import threading
import yolo_opencv

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
# host_ip = socket.gethostbyname(host_name)
host_ip = "10.3.77.117"
print('HOST IP:', host_ip)
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
    camera_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host_ip = "10.3.77.133"
    port = 9999
    camera_socket.connect((host_ip, port))
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = camera_socket.recv(4*1024)
            if not packet: break
            data+=packet
        packet_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packet_msg_size)[0]

        while len(data) < msg_size:
            data+= camera_socket.recv(4*1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
    camera_socket.close()
    
thread = threading.Thread(target=start_video_stream, args=())
thread.start()

def serve_client(addr, client_socket):
    global frame
    try:
        print("Client {} CONNECTED".format(addr))
        if client_socket:
            while True:

                frameClient = yolo_opencv.image_analyzer(frame)
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