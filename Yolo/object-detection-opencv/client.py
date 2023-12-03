import socket, cv2, pickle, struct, traceback

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = "127.0.0.1"
port = 9999
socket_address = (host_ip, port)
payload_size = struct.calcsize("Q")

def receive_video_stream():
    try:
        server_socket.connect(socket_address)
        print('Connected to server')
        data=b""
        while True:
            try:
                while len(data) < payload_size:
                    packet = server_socket.recv(4*1024)
                    if not packet: break
                    data+=packet
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
            except Exception as e:
                print(f"Error connected: {e}")
                traceback.print_exc()
                break
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
    finally:
        server_socket.close()

receive_video_stream()