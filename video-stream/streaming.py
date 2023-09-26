import cv2

video_path = 'videoTeste.mp4'
cap = cv2.VideoCapture(video_path)

rtsp_url = 'rtsp://localhost:554/videoTeste.mp4'  
fourcc = cv2.VideoWriter_fourcc(*'H264')  # Not clear yet
out = cv2.VideoWriter(rtsp_url, fourcc, 30, (480, 480))  


while True:
    ret, frame = cap.read() 

    if not ret:
        break

    # out.write(frame)  # Transmite o frame para o servidor RTSP

    cv2.imshow('Video', frame)  # Exibe o vídeo localmente

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
