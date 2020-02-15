# This a modifed version of the webstreaming module refrenced in an article by PyImageSearch

from pyimagesearch.motion_detection import SingleMotionDetector
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import datetime
import imutils
import time
import cv2
from Databases.face_encodings_database import FaceEncodingsDatabase as fed
from Camera import Match_Faces_From_Feed as webcamThingy
from Databases.Database_Coms import  DatabaseComs
from Logging.Logger import Logger
from Visuals_Processing.image_utils import ImageUtils


outputFrame = None
lock = threading.Lock()


app = Flask(__name__)

# vs = VideoStream(usePiCamera=1).start()
vs = VideoStream(src=0).start()
time.sleep(2.0)

# offset_percentage will be added to a settings database
offset_percentage = 0.5


# Create an instance of the logger module
logger = Logger()





@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")


def detect_motion(frameCount):
    global vs, outputFrame, lock

    # These lines ideally should be moved, only kept here for testing purposes ##
    Database_Coms_obj = DatabaseComs()
    fed_obj = fed(logger)

    Database_Coms_obj.init_db_tables()

    fed_obj.load_database()
    fed_obj.debug_print_names()

    match_face_from_feed = webcamThingy.MatchFaceFromFeed(logger)
    ########################################################

    # initialize the motion detector and the total number of frames
    # accumWeight will be added to a settings database
    md = SingleMotionDetector(accumWeight=0.5)
    total = 0

    # loop over frames from the video stream
    while True:
        # read the next frame from the video stream, resize it,
        # convert the frame to grayscale, and blur it
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        cropped_gray = ImageUtils.crop_bottom_half(gray, offset_percentage)

        # grab the current timestamp and draw it on the frame
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime(
            "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        # if the total number of frames has reached a sufficient
        # number to construct a reasonable background model, then
        # continue to process the frame
        if total > frameCount:
            # detect motion in the image
            motion = md.detect(cropped_gray)

            # check to see if motion was found in the frame
            if motion is not None:
                # unpack the tuple and draw the box surrounding the
                # "motion area" on the output frame
                (thresh, (minX, minY, maxX, maxY)) = motion
                cv2.rectangle(frame, (minX, minY + int(gray.shape[0] * offset_percentage)), (maxX, maxY),
                              (0, 0, 255), 2)
                # If motion is detected, run the frame through the facial detection algorithm
                match_face_from_feed.get_face_matches(frame)


        # update the background model and increment the total number
        # of frames read thus far
        md.update(cropped_gray)
        total += 1

        # acquire the lock, set the output frame, and release the
        # lock
        with lock:
            outputFrame = frame.copy()


def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock

    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue

            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage.tobytes()) + b'\r\n')


@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


# check to see if this is the main thread of execution
if __name__ == '__main__':

    # The ip and port will possibly be added to the settings table in the database
    ip = "0.0.0.0"
    port = "8000"
    frame_count = 24

    # start a thread that will perform motion detection
    t = threading.Thread(target=detect_motion, args=(
        frame_count,))
    t.daemon = True
    t.start()

    # start the flask app
    app.run(host=ip, port=port, debug=True,
            threaded=True, use_reloader=False)

# release the video stream pointer
vs.stop()