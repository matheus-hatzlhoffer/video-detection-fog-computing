import socket, cv2, pickle, struct


def recieveVideo():

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_ip = "127.0.0.1"
        port = 9997
        client_socket.connect((host_ip, port))

        data = b""
        payload_size=struct.calcsize("Q")
        while True:
            while len(data) < payload_size:
                print('a')
                packet = client_socket.recv(4*1024)
                if not packet: 
                    print('maracuja')
                    break
                data+=packet
                print('c')
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            print("d")
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data ) < msg_size:
                print('b')
                data += client_socket.recv(4*1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            cv2.imshow("Recieving video from server", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        client_socket.close()
    except Exception as e:
        print(e)

while(True):
    recieveVideo()