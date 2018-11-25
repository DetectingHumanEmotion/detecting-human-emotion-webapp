import cv2
import datetime
import tensorflow as tf
from scipy.spatial import distance as dist
from multiprocessing import Queue, Pool,Process #used for multiprocessing
from threading import Thread #used for threading
from imutils import face_utils
import dlib

try:
    from utilities.detector_utils import WebcamVideoStream
    from utilities import detector_utils

except ModuleNotFoundError:
    from .utilities.detector_utils import WebcamVideoStream
    from .utilities import detector_utils


def eye_aspect_ratio(eye):
	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])

	# compute the euclidean distance between the horizontal
	# eye landmark (x, y)-coordinates
	C = dist.euclidean(eye[0], eye[3])

	# compute the eye aspect ratio
	ear = (A + B) / (2.0 * C)

	# return the eye aspect ratio
	return ear




frame_processed = 0
score_thresh = 0.2

# Create a worker thread that loads graph and
# does detection on images in an input queue and puts it on an output queue

def worker(input_q, output_q, cap_params, frame_processed):
    print(">> loading frozen model for worker")
    detection_graph, sess = detector_utils.load_inference_graph()
    sess = tf.Session(graph=detection_graph)
    while True:
        #print("> ===== in worker loop, frame ", frame_processed)
        frame = input_q.get()
        if (frame is not None):
            # actual detection
            boxes, scores = detector_utils.detect_objects(
                frame, detection_graph, sess)
            # draw bounding boxes
            detector_utils.draw_box_on_image(
                cap_params['num_hands_detect'], cap_params["score_thresh"], scores, boxes, cap_params['im_width'], cap_params['im_height'], frame)
            # add frame annotated with bounding box to queue
            output_q.put(frame)
            frame_processed += 1
        else:
            output_q.put(frame)
    sess.close()

def record():
    # To run program run the following in cli from this directory
    # python detect_multi_threaded.py --source 0 --shape-predictor shape_predictor_68_face_landmarks.dat


    # parser = argparse.ArgumentParser()
    # parser.add_argument('-src', '--source', dest='video_source', type=int,
    #                     default=0, help='Device index of the camera.')
    # parser.add_argument('-nhands', '--num_hands', dest='num_hands', type=int,
    #                     default=2, help='Max number of hands to detect.')
    # parser.add_argument('-fps', '--fps', dest='fps', type=int,
    #                     default=1, help='Show FPS on detection/display visualization')
    # parser.add_argument('-wd', '--width', dest='width', type=int,
    #                     default=300, help='Width of the frames in the video stream.')
    # parser.add_argument('-ht', '--height', dest='height', type=int,
    #                     default=200, help='Height of the frames in the video stream.')
    # parser.add_argument('-ds', '--display', dest='display', type=int,
    #                     default=1, help='Display the detected images using OpenCV. This reduces FPS')
    # parser.add_argument('-num-w', '--num-workers', dest='num_workers', type=int,
    #                     default=4, help='Number of workers.')
    # parser.add_argument('-q-size', '--queue-size', dest='queue_size', type=int,
    #                     default=5, help='Size of the queue.')
    # parser.add_argument("-p", "--shape-predictor", required=True,
    #                 help="path to facial landmark predictor")
    # parser.add_argument("-v", "--video", type=str, default="",
    #                 help="path to input video file")
    # args = parser.parse_args()


    # define two constants, one for the eye aspect ratio to indicate
    # blink and then a second constant for the number of consecutive
    # frames the eye must be below the threshold
    EYE_AR_THRESH = 0.3
    EYE_AR_CONSEC_FRAMES = 3

    # initialize the frame counters and the total number of blinks
    TOTAL_BLINKS = 0

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    # ags=vars(args)
    # predictor = dlib.shape_predictor(ags["shape_predictor"])
    predictor = dlib.shape_predictor("visual/shape_predictor_68_face_landmarks.dat")

    # grab the indexes of the facial landmarks for the left and
    # right eye, respectively
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    # (leftjawstart,rightjawend)  = face_utils.FACIAL_LANDMARKS_IDXS["jaw"]

    # input_q = Queue(maxsize=args.queue_size)
    # output_q = Queue(maxsize=args.queue_size)
    input_q = Queue(maxsize=5)
    output_q = Queue(maxsize=5)

    # video_capture = WebcamVideoStream(src=args.video_source,
    #                                   width=args.width,
    #                                   height=args.height).start()
    video_capture = WebcamVideoStream(src=0,
                                      width=300,
                                      height=200).start()
    cap_params = {}
    frame_processed = 0
    cap_params['im_width'], cap_params['im_height'] = video_capture.size()
    cap_params['score_thresh'] = score_thresh

    # max number of hands we want to detect/track
    # cap_params['num_hands_detect'] = args.num_hands
    cap_params['num_hands_detect'] = 2

    # print(cap_params, args)

    # spin up workers to paralleize detection.
    # pool = Pool(args.num_workers, worker,
    #             (input_q, output_q, cap_params, frame_processed))
    pool = Pool(4, worker,
                (input_q, output_q, cap_params, frame_processed))


    num_frames = 0
    fps = 0
    index = 0
    BLINK_COUNTER = 0
    TOTAL_BLINKS = 0
    show_display =1
    show_fps = 1
    show_blinks = 1
    if(show_display>0):
        cv2.namedWindow('Multi-Threaded Detection', cv2.WINDOW_NORMAL)
    start_time = datetime.datetime.now()
    while True:
        frame = video_capture.read()
        frame = cv2.flip(frame, 1)
        index += 1

        input_q.put(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        output_frame = output_q.get()

        gray = cv2.cvtColor(output_frame, cv2.COLOR_BGR2GRAY)
        output_frame = cv2.cvtColor(output_frame, cv2.COLOR_RGB2BGR)

        # if first == True:
        #     detector_utils.draw_face(args.width, args.height, output_frame)       ##  TEST DRAWING THE FACE   #####
        #     first = False
        elapsed_time = (datetime.datetime.now() -
                        start_time).total_seconds()
        num_frames += 1
        fps = num_frames / elapsed_time
        # print("frame ",  index, num_frames, elapsed_time, fps)

        if (output_frame is not None):

            # detect faces in the grayscale frame
            rects = detector(gray, 0)

            # loop over the face detections
            for rect in rects:
                # determine the facial landmarks for the face region, then
                # convert the facial landmark (x, y)-coordinates to a NumPy
                # array
                # print("rect type: ", type(rect))
                # print("output_frame type: ", type(output_frame))
                shape = predictor(output_frame, rect)
                shape = face_utils.shape_to_np(shape)

                # extract the left and right eye coordinates, then use the
                # coordinates to compute the eye aspect ratio for both eyes
                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]
                leftEAR = eye_aspect_ratio(leftEye)
                rightEAR = eye_aspect_ratio(rightEye)
                jaw = shape[0:17]

                # average the eye aspect ratio together for both eyes
                ear = (leftEAR + rightEAR) / 2.0

                # compute the convex hull for the left and right eye, then
                # visualize each of the eyes
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                cv2.drawContours(output_frame, [leftEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(output_frame, [rightEyeHull], -1, (0, 255, 0), 1)

                # check to see if the eye aspect ratio is below the blink
                # threshold, and if so, increment the blink frame counter
                if ear < EYE_AR_THRESH:
                    BLINK_COUNTER += 1

                # otherwise, the eye aspect ratio is not below the blink
                # threshold
                else:
                    # if the eyes were closed for a sufficient number of
                    # then increment the total number of blinks
                    if BLINK_COUNTER >= EYE_AR_CONSEC_FRAMES:
                        TOTAL_BLINKS += 1

                    # reset the eye frame counter
                    BLINK_COUNTER = 0

            # if (args.display > 0):
            #     if (args.fps > 0):
            if (show_display > 0):
                if (show_fps > 0):
                    detector_utils.draw_fps_on_image("FPS : " + str(int(fps)), output_frame)

                    # center=( int(args.width/2), int(args.height/2))
                    # cv2.ellipse(output_frame,center , (45, 85), 0, 0, 180, 255, 1)
                    face_pts = cv2.ellipse2Poly((150, 100), (45, 85), 0, 0, 180, 5)
                    cv2.polylines(output_frame, [face_pts], 1, (0, 255, 0))
                if (show_blinks > 0):
                    # draw the total number of blinks on the frame along with
                    # the computed eye aspect ratio for the frame
                    cv2.putText(output_frame, "Blinks: {}".format(TOTAL_BLINKS), (50, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.putText(output_frame, "EAR: {:.2f}".format(ear), (200, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


                cv2.imshow('Multi-Threaded Detection', output_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                if (num_frames == 400):
                    num_frames = 0
                    start_time = datetime.datetime.now()
                else:
                    print("frames processed: ", index, "elapsed time: ",
                          elapsed_time, "fps: ", str(int(fps)))

        else:
            # print("video end")
            break
    elapsed_time = (datetime.datetime.now() -
                    start_time).total_seconds()
    fps = num_frames / elapsed_time
    print("fps", fps)
    pool.terminate()
    video_capture.stop()
    cv2.destroyAllWindows()


if __name__ == '__main__':


    ## Multiprocessing way
    try:
        process1 = Process(target=record)

        process2 = Process(target=run_audio_deception_stream)

        process1.start()
        print("Proecss 1 started")
        process2.start()
        print("Process 2 started")

        process1.join()
        process2.join()

    except:
        print("process failed")

    ## This is the Threading way
    # try:
    #     thread1 = threading.Thread(target=record)
    #
    #     thread2 = threading.Thread(target=run)
    #
    #
    #     thread1.start()
    #      print("Thread 1 started")
    #     thread2.start()
    #     print("Thread 2 started")
    #
    #     thread1.join()
    #     thread2.join()
    #
    # except:
    #     print("Thread failed")

