# Utilities for object detector.

import numpy as np
import sys
import tensorflow as tf
import os
from threading import Thread
from datetime import datetime
import cv2
from utils import label_map_util
from collections import defaultdict


# void cv::ellipse2Poly	(	Point 	center,
# Size 	axes,
# int 	angle,
# int 	arcStart,
# int 	arcEnd,
# int 	delta,
# std::vector< Point > & 	pts
# )
# Approximates an elliptic arc with a polyline.
#
# The function ellipse2Poly computes the vertices of a polyline that approximates the specified elliptic arc. It is used by cv::ellipse.
#
# Parameters
# center	Center of the arc.
# axes	Half of the size of the ellipse main axes. See the ellipse for details.
# angle	Rotation angle of the ellipse in degrees. See the ellipse for details.
# arcStart	Starting angle of the elliptic arc in degrees.
# arcEnd	Ending angle of the elliptic arc in degrees.
# delta	Angle between the subsequent polyline vertices. It defines the approximation accuracy.
# pts	Output vector of polyline vertices.

detection_graph = tf.Graph()
sys.path.append("..")

# score threshold for showing bounding boxes.
_score_thresh = 0.27

MODEL_NAME = 'hand_inference_graph'
# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join(MODEL_NAME, 'hand_label_map.pbtxt')

NUM_CLASSES = 1
# load label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(
    label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Load a frozen infrerence graph into memory
def load_inference_graph():

    # load frozen tensorflow model into memory
    print("> ====== loading HAND frozen graph into memory")
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
        sess = tf.Session(graph=detection_graph)
    print(">  ====== Hand Inference graph loaded.")
    
    return detection_graph, sess
# def draw_face(width,height,image_np):
#     center_x = width/2
#     center_y = height/2
#     print("Center: " , center_x, " , " , center_y)
#     cv2.ellipse(image_np,(150,100),(45,85),0,  0,180,255, 1)
#     return face_pts
#
#     # print(face_pts)
#     # int 	delta,
#     # std::vector< Point > & 	pts
#     # )
# 	#	(InputOutputArray img, Point center, Size axes, double 	angle,
# 	# double startAngle, double endAngle, const Scalar &color,
# 	# int thickness = 1, int lineType = LINE_8, int shift = 0 )
# 	 #One argument is the center location (x,y).
# 	 #Next argument is axes lengths (major axis length, minor axis length).
# 	 #angle is the angle of rotation of ellipse in anti-clockwise direction.
# 	 #startAngle and endAngle denotes the starting and ending of ellipse arc measured in clockwise direction from major axis. i.e. giving values 0 and 360 gives the full ellipse.


# print(im_width,im_height)
# cv2.ellipse(image_np, (im_width/2, im_height/2), (45, 85), 0, 0, 180, 255, 1)
# face_pts = cv2.ellipse2Poly(((im_width / 2), (im_height / 2)), (45, 85), 0, 0, 180, 5)
# number_of_points = len(face_pts)

face_pts = cv2.ellipse2Poly( (150,100), (45, 85), 0, 0, 180, 5)
# cv2.polylines(,1,RGBA(0.,1.,0.,1.))
number_of_points = len(face_pts)

# print(face_pts)
# (x,y)=face_pts
# print("x:",x,"y:",y)
# print("THIRDDDDDDDDDDDDDDDD: ",face_pts[3])
# draw the detected bounding boxes on the images
# You can modify this to also draw a label.
def draw_box_on_image(num_hands_detect, score_thresh, scores, boxes, im_width, im_height, image_np):
    cv2.ellipse(image_np, (150, 100), (45, 85), 0, 0, 180, 255, 1)
    for i in range(num_hands_detect):
        if (scores[i] > score_thresh):
            (left, right, top, bottom) = (boxes[i][1] * im_width, boxes[i][3] * im_width,
                                          boxes[i][0] * im_height, boxes[i][2] * im_height)
            p1 = (int(left), int(top))
            p2 = (int(right), int(bottom))
            cv2.rectangle(image_np, p1, p2, (77, 255, 9), 3, 1)
            # print(number_of_points)

            j=0

            while j < (number_of_points/4+4):
                (x1, y1) = face_pts[j]
                (x2, y2) = face_pts[j+1]
                (x3, y3) = face_pts[-j-2]
                (x4, y4) = face_pts[-j-1]
                """
                x4,y4 -- x1,y1          L,T -- L+(R-L/2),T -- R,T
                  |        |             |                     |
                x3,y3 -- x2,y2        L,T+(B-T/2)          R,T+(B-T/2)
                """
                # print(i,face_pts[i], face_pts[i+1],face_pts[-i-1], face_pts[-i])
                x_half = (right - left) / 2
                y_half = (bottom - top) / 2

                xx = left
                yy = top
                if ((xx <= x2) and (xx >= x3) and (yy >= y1) and (yy <= y2)):
                    print("found" , str(datetime.now()))

                xx = left + x_half
                if ((xx <= x2) and (xx >= x3) and (yy >= y1) and (yy <= y2)):
                    print("found", str(datetime.now()))

                xx = right
                yy = top
                if ((xx <= x2) and (xx >= x3) and (yy >= y1) and (yy <= y2)):
                    print("found", str(datetime.now()))

                xx = left
                yy = top + y_half
                if ((xx <= x2) and (xx >= x3) and (yy >= y1) and (yy <= y2)):
                    print("found", str(datetime.now()))

                xx = right
                yy = top + y_half
                if ((xx <= x2) and (xx >= x3) and (yy >= y1) and (yy <= y2)):
                    print("found", str(datetime.now()))

                j = j+1

            # for face_pt in face_pts:
            #     (x,y)=face_pt
            #     # if (p1==(x,y)) or (p2==(x,y)):
            #     if (x>left) and (x<right) and (y<top) and (y>bottom):
            # # if np.logical_and(p1, face_pts):
            #         print("hand touched face")
            #         print("Top left corner: ", p1)
            #         print("Bottom right corner: ", p2)
            #         print("--------------")
    # p1 = (int (0), int (0))
    # p2 = (int (50), int (100))
    # cv2.rectangle(image_np, p1, p2, (77, 255, 9), 3, 1)


# Show fps value on image.d
def draw_fps_on_image(fps, image_np):
    cv2.putText(image_np, fps, (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (77, 255, 9), 2)


# Actual detection .. generate scores and bounding boxes given an image
def detect_objects(image_np, detection_graph, sess):
    # Definite input and output Tensors for detection_graph
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    # Each box represents a part of the image where a particular object was detected.
    detection_boxes = detection_graph.get_tensor_by_name(
        'detection_boxes:0')
    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    detection_scores = detection_graph.get_tensor_by_name(
        'detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name(
        'detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name(
        'num_detections:0')

    image_np_expanded = np.expand_dims(image_np, axis=0)

    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores,
            detection_classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})
    return np.squeeze(boxes), np.squeeze(scores)


# Code to thread reading camera input.
# Source : Adrian Rosebrock
# https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/
class WebcamVideoStream:
    def __init__(self, src, width, height):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        (self.grabbed, self.frame) = self.stream.read()

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def size(self):
        # return size of the capture device
        return self.stream.get(3), self.stream.get(4)

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
