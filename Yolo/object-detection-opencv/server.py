import socket, cv2, pickle, struct
import threading
import yolo_opencv
import time
import numpy as np

f = open("logfile_server_recieve.csv", "w")
f.write(str("FPS,Frame,Code,Time,bitrate,frametime\n"))

g = open("logfile_server_send.csv", "w")
g.write(str("FPS,Frame,Code,Time,bitrate,frametime\n"))


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
frame_ID = struct.pack("P",-1)
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
            frame_count_fps = 0
            frame_count = 0
            fps = 0
            
            start_time_2 = time.time()    

            data = b""
            payload_size = struct.calcsize("Q")
            code_payload = struct.calcsize("P")
            while True:
                start_time = time.time()

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
                frame_count += 1
                frame_count_fps += 1

                elapsed_time = time.time() - start_time_2

                if elapsed_time > 1:
                    fps = frame_count_fps / elapsed_time
                    print(f"FPS rec: {fps:.2f}")                    
                    frame_count_fps = 0
                    start_time_2 = time.time()
                end_time = time.time()

                
                f.write(str(str(fps)+","+str(frame_count)+","+str(struct.unpack("P", frame_ID)[0]).zfill(12)+","+str(end_time-start_time)+","+str((msg_size)/(end_time-start_time))+","+str(time.time())+"\n"))

                # frame = ssd.consulta_SSD(frame, net, CLASSES, COLORS)
                # frame = yolo_opencv.image_analyzer(frame)
                # cv2.imshow("RECIEVING VIDEO", frame)
                # key = cv2.waitkey(1) & 0xFF
                # if key == ord('q'):
                #     break

            camera_2_socket.close()
        except Exception as e:
            # print(e)
            print(f"Camera {addr} disconnected")
            frame_ID = struct.pack("P",-1)
            pass

thread = threading.Thread(target=start_video_stream, args=())
thread.start()

def serve_client(addr, client_socket):
    last_frame = struct.pack("P",-1)
    global frame
    global frame_ID
    try:
        print("Client {} CONNECTED".format(addr))
        if client_socket:
            frame_count_fps = 0
            frame_count = 0
            fps = 0

            start_time_2 = time.time()    
            while True:
                if last_frame != frame_ID:
                    start_time = time.time()
                    frame_count += 1
                    try:
                        frameClient = yolo_opencv.image_analyzer(frame)
                    except Exception as ex:
                        frameClient = np.zeros(shape=[360, 640, 3], dtype=np.uint8) 
                    a = pickle.dumps(frameClient)
                    message = struct.pack("Q", len(a))+frame_ID+a
                    client_socket.sendall(message)
                    frame_count_fps += 1

                    elapsed_time = time.time() - start_time_2

                    if elapsed_time > 1:
                        fps = frame_count_fps / elapsed_time
                        print(f"FPS send: {fps:.2f}")                    
                        frame_count_fps = 0
                        start_time_2 = time.time()
                    last_frame = frame_ID

                    end_time = time.time()
                    g.write(str(str(fps)+","+str(frame_count)+","+str(struct.unpack("P", frame_ID)[0]).zfill(12)+","+str(end_time-start_time)+","+str(len(message)/(end_time-start_time))+","+str(time.time())+"\n"))

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