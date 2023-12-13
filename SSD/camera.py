import socket, cv2, pickle, struct
import imutils
import cv2
import time
f = open("logfile_camera.csv", "w")


def start_video_stream():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # host_ip = "127.0.0.1"
    # host_ip = "192.168.0.131"
    host_ip = "10.3.77.135"
    
    port = 9999
    socket_address = (host_ip, port)
    frame_count = 0


    camera = False
    if camera == True:
        vid = cv2.VideoCapture(0)
    else:
        vid = cv2.VideoCapture("LondonBikeRideCityTour2022.mp4")
        # vid = cv2.VideoCapture("videoTeste.mp4")
    try:
        server_socket.connect(socket_address)
        print('Connected to server')
        frame_count_fps = 0
        start_time_2 = time.time()    


        while(vid.isOpened()):
            start_time = time.time()
            frame_count += 1
            img, frame = vid.read()
            time.sleep(0.02)
            try:
                frame = imutils.resize(frame, width=240)
            except Exception as ex:
                print("End of Video")
                break
                pass
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a))+struct.pack("P", int(str(frame_count).zfill(12)) )+a
            server_socket.sendall(message)
            frame_count_fps += 1
            elapsed_time = time.time() - start_time_2

            if elapsed_time > 1:
                fps = frame_count_fps / elapsed_time
                print(f"FPS: {fps:.2f}")                    
                frame_count_fps = 0
                start_time_2 = time.time()

            end_time = time.time()
            f.write(str("Frame,"+str(frame_count)+",Code,"+str(frame_count).zfill(12)+",Time,"+str(end_time-start_time)+",bitrate,"+str(len(message)/(end_time-start_time))+",frametime,"+str(time.time())+"\n"))
            # cv2.imshow("Transmitting to server", frame)
            # key = cv2.waitKey(1) & 0xFF
            # if key == ord('q'):
        server_socket.close()
    except Exception as e:
        print(e)
        # print(f"COULDN'T CONECT TO SERVER, TRYING AGAIN")
        pass

while(True):
    start_video_stream()
