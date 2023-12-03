import time
import socket, cv2, pickle, struct, traceback

def receive_video_stream():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = "127.0.0.1"
    port = 9999
    socket_address = (host_ip, port)
    data=b""
    payload_size = struct.calcsize("Q")
    try:
        server_socket.connect(socket_address)
        print('Connected to server')
        time.sleep(5)
        while True:
            # try:
            while len(data) < payload_size:
                packet = server_socket.recv(4*1024)
                print("estou no looping")
                if not packet: break
                data+=packet
            if(len(data)> 0):
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]
                while len(data ) < msg_size:
                    data += server_socket.recv(4*1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)
                cv2.imshow("Recieving video from server", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
            # except Exception as e:
            #     print(f"Error connected: {e}")
            #     print("packed_msg_size ", packed_msg_size)
            #     print("payload_size ", payload_size)
            #     print("data ", data)
            #     traceback.print_exc()
            #     break
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
    finally:
        print("closing socket")
        server_socket.close()

receive_video_stream()