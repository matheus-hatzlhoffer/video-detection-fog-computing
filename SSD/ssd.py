# import the necessary packages
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import cv2
# # construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-p", "--prototxt", required=True,
# 	help="path to Caffe 'deploy' prototxt file")
# ap.add_argument("-m", "--model", required=True,
# 	help="path to Caffe pre-trained model")
# ap.add_argument("-i", "--input", type=str, default="",
# 	help="path to (optional) input video file")
# ap.add_argument("-o", "--output", type=str, default="",
# 	help="path to (optional) output video file")
# ap.add_argument("-d", "--display", type=int, default=1,
# 	help="whether or not output frame should be displayed")
# ap.add_argument("-c", "--confidence", type=float, default=0.2,
# 	help="minimum probability to filter weak detections")
# ap.add_argument("-u", "--use-gpu", type=bool, default=False,
# 	help="boolean indicating if CUDA GPU should be used")
# args = vars(ap.parse_args())

def load_model():
	# initialize the list of class labels MobileNet SSD was trained to
	# detect, then generate a set of bounding box colors for each class
	CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
		"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
		"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
		"sofa", "train", "tvmonitor"]
	COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))  
	prototxt = "MobileNetSSD_deploy.prototxt"
	model = "MobileNetSSD_deploy.caffemodel"
	use_gpu = 1

	# load our serialized model from disk
	net = cv2.dnn.readNetFromCaffe(prototxt, model)
	# check if we are going to use GPU
	if use_gpu:
		# set CUDA as the preferable backend and target
		print("[INFO] setting preferable backend and target to CUDA...")
		net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
		net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
	return net, CLASSES, COLORS

# initialize the video stream and pointer to output video file, then
# start the FPS timer
# print("[INFO] accessing video stream...")
# vs = cv2.VideoCapture(args["input"] if args["input"] else 0)
# writer = None
# fps = FPS().start()
# loop over the frames from the video stream
# while True:
	# read the next frame from the file
	# (grabbed, frame) = vs.read()
	# if the frame was not grabbed, then we have reached the end
	# of the stream
	# if not grabbed:
		# break
	# resize the frame, grab the frame dimensions, and convert it to
	# a blob
def consulta_SSD(frame, net, CLASSES, COLORS):
	
	frame = imutils.resize(frame, width=240)
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
	# pass the blob through the network and obtain the detections and
	# predictions
	net.setInput(blob)
	detections = net.forward()
	# loop over the detections
	for i in np.arange(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the prediction
		confidence = detections[0, 0, i, 2]
		# filter out weak detections by ensuring the `confidence` is
		# greater than the minimum confidence
		if confidence > 0.2:
			# extract the index of the class label from the
			# `detections`, then compute the (x, y)-coordinates of
			# the bounding box for the object
			idx = int(detections[0, 0, i, 1])
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")
			# draw the prediction on the frame
			label = "{}: {:.2f}%".format(CLASSES[idx],
				confidence * 100)
			cv2.rectangle(frame, (startX, startY), (endX, endY),
				COLORS[idx], 2)
			y = startY - 15 if startY - 15 > 15 else startY + 15
			cv2.putText(frame, label, (startX, y),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
	# show the output frame
	cv2.imshow("Frame", frame)
	return frame		
    # check to see if the output frame should be displayed to our
	# # screen
	# if args["display"] > 0:
	# 	# show the output frame
	# 	cv2.imshow("Frame", frame)
	# 	key = cv2.waitKey(1) & 0xFF
	# 	# if the `q` key was pressed, break from the loop
	# 	if key == ord("q"):
	# 		break
	# if an output video file path has been supplied and the video
	# writer has not been initialized, do so now
	# if args["output"] != "" and writer is None:
	# 	# initialize our video writer
	# 	fourcc = cv2.VideoWriter_fourcc(*"MJPG")
	# 	writer = cv2.VideoWriter(args["output"], fourcc, 30,
	# 		(frame.shape[1], frame.shape[0]), True)
	# # if the video writer is not None, write the frame to the output
	# # video file
	# if writer is not None:
	# 	writer.write(frame)
	# update the FPS counter
	# fps.update()
# stop the timer and display FPS information
# fps.stop()
# print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
# print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
