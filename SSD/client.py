import socket, cv2, pickle, struct, time


def recieveVideo():

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # host_ip = "127.0.0.1"
        # host_ip = "192.168.0.131"
        host_ip = "10.3.77.135"

        port = 9997
        client_socket.connect((host_ip, port))
        frame_count = 0

        f = open("logfile_client.txt", "w")

        data = b""
        payload_size=struct.calcsize("Q")
        while True:
            start_time = time.time()
            while len(data) < payload_size:
                packet = client_socket.recv(4*1024)
                if not packet: 
                    break
                data+=packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data ) < msg_size:
                data += client_socket.recv(4*1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            cv2.imshow("Recieving video from server", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            frame_count += 1
            end_time = time.time()
            f.write(str("Frame: "+str(frame_count)+" Time: "+str(end_time-start_time)+" bitrate: "+str(len(data)/(end_time-start_time))+" frametime: "+str(time.time())+"\n"))
        client_socket.close()
    except Exception as e:
        print(e)

while(True):
    recieveVideo()
