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
        frame_count_fps = 0
        fps=0

        f = open("logfile_client.csv", "w")
        f.write(str("FPS,Frame,Code,Time,bitrate,frametime\n"))

        data = b""
        payload_size=struct.calcsize("Q")
        code_payload = struct.calcsize("P")
        start_time_2 = time.time()    
        while True:
            start_time = time.time()
            while len(data) < payload_size+code_payload:
                packet = client_socket.recv(4*1024)
                if not packet: 
                    break
                data+=packet
            packed_msg_size = data[:payload_size]
            code = data[payload_size:payload_size+code_payload]
            # print(struct.unpack("P", code)[0])
            data = data[payload_size+code_payload:]
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
            frame_count_fps += 1

            elapsed_time = time.time() - start_time_2
            if elapsed_time > 1:
                fps = frame_count_fps / elapsed_time
                print(f"FPS: {fps:.2f}")                    
                frame_count_fps = 0
                start_time_2 = time.time()
            end_time = time.time()
            f.write(str(str(fps)+","+str(frame_count)+","+str(struct.unpack("P", code)[0]).zfill(12)+","+str(end_time-start_time)+","+str((msg_size)/(end_time-start_time))+","+str(time.time())+"\n"))
        client_socket.close()
    except Exception as e:
        print(e)

while(True):
    recieveVideo()
