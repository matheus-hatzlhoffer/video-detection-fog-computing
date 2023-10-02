import cv2

video_path = 'videos/LondonBikeRideCityTour2022.mp4'
cap = cv2.VideoCapture(video_path)

rtmp_url = 'rtmp://localhost:1935/'  
fourcc = cv2.VideoWriter_fourcc(*'avc1')  # Not clear yet
out = cv2.VideoWriter(rtmp_url, fourcc, 30, (480, 480))  


while True:
    ret, frame = cap.read() 

    if not ret:
        break

    out.write(frame)  # Transmite o frame para o servidor RTMP

    # cv2.imshow('Video', frame)  # Exibe o vídeo localmente

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
# cv2.destroyAllWindows()
